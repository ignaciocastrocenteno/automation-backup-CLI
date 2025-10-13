# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

from pathlib import Path
import tempfile
from automation_backup_cli.domain.models import BackupJob
from automation_backup_cli.services.backup_service import execute_backup


def test_dry_run_collects_files_without_copying(tmp_path: Path):
    # Arrange: create fake source files
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    (src / "a").mkdir(parents=True)
    (src / "a" / "file1.txt").write_text("hello")
    (src / "file2.log").write_text("x")
    dst.mkdir()

    job = BackupJob(
        source=str(src),
        destination=str(dst),
        exclude_patterns=["*.log"],
        compress_format=None,
        dry_run=True,
    )

    # Act
    result = execute_backup(job)

    # Assert
    assert len(result.files_planned) == 1  # file1.txt only
    assert result.files_copied == []       # dry-run -> no copies
