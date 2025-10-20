# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

from pathlib import Path
from freezegun import freeze_time
from zipfile import ZipFile

from automation_backup_cli.domain.models import BackupJob
from automation_backup_cli.services.backup_service import execute_backup

@freeze_time("2025-10-14 12:00:00")
def test_execute_backup_with_zip_creates_archive(tmp_path: Path):
    src = tmp_path / "src"; dst = tmp_path / "dst"
    (src / "dir").mkdir(parents=True)
    (src / "dir" / "a.txt").write_text("A")
    dst.mkdir()

    job = BackupJob(
        source=str(src),
        destination=str(dst),
        exclude_patterns=[],
        compress_format="zip",
        dry_run=False,
    )

    result = execute_backup(job)
    assert result.compressed_artifact is not None
    archive = Path(result.compressed_artifact)
    assert archive.exists()
    assert archive.suffix == ".zip"

    # The archive should contain the dated folder structure and file
    with ZipFile(archive, "r") as zf:
        names = zf.namelist()
        assert any(name.endswith("2025/10/14/dir/a.txt") for name in names)
