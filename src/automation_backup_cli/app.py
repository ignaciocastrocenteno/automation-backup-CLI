# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations
from typing import List, Optional

from .domain.models import BackupJob, BackupResult, CompressionFormat
from .services.backup_service import execute_backup
from .adapters.logging_config import setup_logging


def run_backup_job(
    source: str,
    destination: str,
    exclude_patterns: List[str],
    compress_format: Optional[CompressionFormat],
    dry_run: bool,
    verbose: bool,
    retention_days: int | None = None,
) -> BackupResult:
    """
    Application layer: build the domain job and delegate to service.
    Keeps CLI (I/O) separate from domain logic (testable).
    """
    setup_logging(verbose=verbose)
    job = BackupJob(
        source=source,
        destination=destination,
        exclude_patterns=exclude_patterns or [],
        compress_format=compress_format,
        dry_run=dry_run,
        retention_days=retention_days,
    )
    return execute_backup(job)
