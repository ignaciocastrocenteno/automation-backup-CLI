# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

import logging
from typing import List

from ..domain.models import BackupJob, BackupResult, PlanItem, PlanResult
from ..domain.exceptions import InvalidPathError
from ..adapters.filesystem import validate_directory, collect_files, ensure_destination
from ..utils.timeutils import dated_subfolder
from ..services.compression import create_archive

log = logging.getLogger(__name__)


def execute_backup(job: BackupJob) -> BackupResult:
    """
    Execute the backup:
    - Validate and collect files
    - Copy into destination/YYYY/MM/DD
    - Optionally create an archive (zip or tar.gz)
    """
    result = BackupResult()

    try:
        src = validate_directory(job.source)
        dst_root = validate_directory(job.destination)
    except FileNotFoundError as e:
        raise InvalidPathError(str(e)) from e

    files = collect_files(src, job.exclude_patterns)
    dated = dst_root / dated_subfolder()

    if job.dry_run:
        log.info("Dry-run: %d files would be copied to %s", len(files), dated)
        result.files_planned = [str(dated / f.relative_to(src)) for f in files]
        return result

    # Ensure destination and copy files
    ensure_destination(dated)
    for f in files:
        rel = f.relative_to(src)
        target = dated / rel
        ensure_destination(target.parent)
        # copy2 preserves metadata (mtime, etc.)
        import shutil

        shutil.copy2(f, target)
        result.files_copied.append(str(target))

    # Optional compression
    if job.compress_format:
        # Timestamp for archive name, e.g., 20251014_120000
        # Reuse mtime of the dated folder or compute from current time
        from datetime import datetime

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        result.compressed_artifact = str(
            create_archive(dst_root, dated, ts, job.compress_format)  # "zip" | "tar"
        )

    return result


def build_backup_plan(job: BackupJob) -> PlanResult:
    """
    Build a dry-run plan (no filesystem changes).
    - Validates paths
    - Collects files (honoring exclude patterns)
    - Computes destination paths under YYYY/MM/DD
    - Returns PlanResult with counts and sizes
    """
    try:
        src = validate_directory(job.source)
        dst_root = validate_directory(job.destination)
    except FileNotFoundError as e:
        raise InvalidPathError(str(e)) from e

    files = collect_files(src, job.exclude_patterns)
    dated_dst = dst_root / dated_subfolder()

    items: List[PlanItem] = []
    total_size = 0
    for f in files:
        rel = f.relative_to(src)
        target = dated_dst / rel
        size = f.stat().st_size
        total_size += size
        items.append(PlanItem(source=str(f), destination=str(target), size_bytes=size))

    return PlanResult(items=items, total_files=len(items), total_size_bytes=total_size)
