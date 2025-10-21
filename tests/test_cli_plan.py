# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations
from pathlib import Path
from typer.testing import CliRunner
from automation_backup_cli.cli import app

runner = CliRunner()


def test_cli_plan_renders_table(tmp_path: Path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    (src / "a").mkdir(parents=True)
    (src / "a" / "file.txt").write_text("hello")
    dst.mkdir()

    result = runner.invoke(app, ["plan", "--source", str(src), "--dest", str(dst)])
    assert result.exit_code == 0
    # Check that table headers or lines appear
    assert "Planned copy" in result.stdout
    assert "Total files:" in result.stdout
