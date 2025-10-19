# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno

from __future__ import annotations

import pytest
from pathlib import Path
from typer.testing import CliRunner
from automation_backup_cli import cli as cli_module

runner = CliRunner()

def test_cli_plan_unexpected_exception_exit_1(monkeypatch, tmp_path: Path):
    """
    Make build_backup_plan raise a RuntimeError to hit the `except Exception` branch.
    Expect exit code 1 and an error message.
    """
    def boom(*args, **kwargs):
        raise RuntimeError("kaboom")

    monkeypatch.setattr(cli_module, "build_backup_plan", boom)

    src = tmp_path / "src"; dst = tmp_path / "dst"
    (src / "a").mkdir(parents=True); (src / "a" / "file.txt").write_text("ok")
    dst.mkdir()

    result = runner.invoke(
        cli_module.app,
        ["plan", "--source", str(src), "--dest", str(dst), "--verbose"],
    )

    assert result.exit_code == 1
    assert "Error:" in result.stdout
