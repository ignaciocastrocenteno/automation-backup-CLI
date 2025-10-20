# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

from pathlib import Path
from freezegun import freeze_time
import tarfile

from automation_backup_cli.domain.models import BackupJob
from automation_backup_cli.services.backup_service import execute_backup

@freeze_time("2025-10-14 12:00:00")
def test_execute_backup_with_tar_creates_archive(tmp_path: Path):
    src = tmp_path / "src"; dst = tmp_path / "dst"
    (src / "dir").mkdir(parents=True)
    (src / "dir" / "a.txt").write_text("A")
    dst.mkdir()

    job = BackupJob(
        source=str(src),
        destination=str(dst),
        exclude_patterns=[],
        compress_format="tar",
        dry_run=False,
    )

    result = execute_backup(job)
    assert result.compressed_artifact is not None
    archive = Path(result.compressed_artifact)
    assert archive.exists()
    assert archive.suffixes[-2:] == [".tar", ".gz"]

    with tarfile.open(archive, "r:gz") as tf:
        names = tf.getnames()
        assert any(name.endswith("2025/10/14/dir/a.txt") for name in names)
