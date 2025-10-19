# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno

from __future__ import annotations

import pytest
from pathlib import Path
from automation_backup_cli.domain.models import BackupJob
from automation_backup_cli.domain.exceptions import InvalidPathError
from automation_backup_cli.services.backup_service import build_backup_plan

def test_build_backup_plan_invalid_source_raises(tmp_path: Path):
    """Ensure invalid source path maps to InvalidPathError."""
    src = tmp_path / "missing"
    dst = tmp_path / "dst"; dst.mkdir()
    job = BackupJob(
        source=str(src),
        destination=str(dst),
        exclude_patterns=[],
        compress_format=None,
        dry_run=True,
    )
    with pytest.raises(InvalidPathError):
        build_backup_plan(job)
