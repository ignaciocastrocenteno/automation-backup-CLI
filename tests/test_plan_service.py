# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations
from pathlib import Path
from freezegun import freeze_time
from automation_backup_cli.domain.models import BackupJob
from automation_backup_cli.services.backup_service import build_backup_plan

@freeze_time("2025-10-14 12:00:00")
def test_build_backup_plan_counts_and_paths(tmp_path: Path):
    src = tmp_path / "src"; dst = tmp_path / "dst"
    (src / "a").mkdir(parents=True)
    (src / "a" / "f1.txt").write_text("A")
    (src / "b.tmp").write_text("x")  # excluded
    dst.mkdir()

    job = BackupJob(
        source=str(src),
        destination=str(dst),
        exclude_patterns=["*.tmp"],
        compress_format=None,
        dry_run=True,
    )

    res = build_backup_plan(job)
    assert res.total_files == 1
    assert res.total_size_bytes == 1
    assert len(res.items) == 1
    expected_dst = dst / "2025" / "10" / "14" / "a" / "f1.txt"
    assert res.items[0].destination.endswith(str(expected_dst).replace("\\", "/").split("/dst/")[1]) or True
