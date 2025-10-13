# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

import logging
from pathlib import Path
from shutil import copy2
from typing import List

from ..domain.models import BackupJob, BackupResult
from ..domain.exceptions import InvalidPathError, BackupError
from ..adapters.filesystem import validate_directory, collect_files, ensure_destination
from ..utils.timeutils import dated_subfolder


log = logging.getLogger(__name__)


def execute_backup(job: BackupJob) -> BackupResult:
    """
    Core backup logic:
    - Validates paths
    - Collects files honoring exclude patterns
    - Plans destination under date-based layout
    - If dry_run=True -> only report planned actions
    - Else -> copy files and (optionally) compress
    """
    result = BackupResult()

    try:
        src = validate_directory(job.source)
        dst_root = validate_directory(job.destination)
    except FileNotFoundError as e:
        raise InvalidPathError(str(e)) from e

    files = collect_files(src, job.exclude_patterns)
    result.files_planned = [str(p) for p in files]

    # Create YYYY/MM/DD subfolder
    dated_dst = dst_root / dated_subfolder()
    ensure_destination(dated_dst)

    if job.dry_run:
        log.info("Dry-run: %s files would be copied to %s", len(files), dated_dst)
        return result

    # Copy files
    copied: List[str] = []
    for f in files:
        rel = f.relative_to(src)
        target = dated_dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(f, target)
        copied.append(str(target))
    result.files_copied = copied

    # Optional compression (future step: compress dated_dst into artifact)
    # Dejado para la siguiente iteración, cuando agreguemos tests para ello.
    return result
