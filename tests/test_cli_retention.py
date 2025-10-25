# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

from pathlib import Path
from freezegun import freeze_time
from typer.testing import CliRunner
from automation_backup_cli.cli import app

runner = CliRunner()


@freeze_time("2025-10-14 12:00:00")
def test_cli_run_with_retention_removes_old(tmp_path: Path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    (src / "folder").mkdir(parents=True)
    (src / "folder" / "a.txt").write_text("A", encoding="utf-8")
    dst.mkdir()
    # simulate an older backup
    old = dst / "2025" / "10" / "01"
    # Create a dated structure
    old.mkdir(parents=True, exist_ok=True)
    (old / "dummy.txt").write_text("x", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "run",
            "--source",
            str(src),
            "--dest",
            str(dst),
            "--retention-days",
            "7",  # 7 days older than 2025-10-14 -> 2025-10-07 cutoff
        ],
    )

    assert result.exit_code == 0
    assert not old.exists()  # pruned
