# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

from pathlib import Path
import tempfile
import pytest
from freezegun import freeze_time
from automation_backup_cli.domain.models import BackupJob
from automation_backup_cli.services.backup_service import execute_backup
from automation_backup_cli.domain.exceptions import InvalidPathError


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

@freeze_time("2025-10-11 12:00:00")
def test_execute_backup_copies_files(tmp_path: Path):
    src = tmp_path / "src"; dst = tmp_path / "dst"
    (src / "dir").mkdir(parents=True)
    (src / "dir" / "a.txt").write_text("A")
    (src / "b.tmp").write_text("B")
    dst.mkdir()

    job = BackupJob(
        source=str(src),
        destination=str(dst),
        exclude_patterns=["*.tmp"],
        compress_format=None,
        dry_run=False,
    )

    result = execute_backup(job)

    # The file should be copied to the destination directory under the YYYY/MM/DD subfolder
    # Frozen time (for testing) -> 2025/10/11
    expected = dst / "2025" / "10" / "11" / "dir" / "a.txt"
    assert expected.exists()
    # Normalize OS-specific separators before asserting membership
    copied_paths = [Path(p).resolve() for p in result.files_copied]
    assert expected.resolve() in copied_paths


def test_execute_backup_invalid_source(tmp_path: Path):
    dst = tmp_path / "dst"; dst.mkdir()
    job = BackupJob(
        source=str(tmp_path / "nope"),
        destination=str(dst),
        exclude_patterns=[],
        compress_format=None,
        dry_run=True,
    )
    with pytest.raises(InvalidPathError):
        execute_backup(job)
