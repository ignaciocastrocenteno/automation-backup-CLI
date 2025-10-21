# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno

from __future__ import annotations
from pathlib import Path
import pytest
import traceback
from typer.testing import CliRunner
from automation_backup_cli.cli import app

runner = CliRunner()


def test_cli_run_success_dry_run(tmp_path: Path):
    # Arrange
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    (src / "a").mkdir(parents=True)
    (src / "a" / "file.txt").write_text("ok")
    dst.mkdir()

    # Act
    # Do NOT pass mix_stderr (not supported in some Click/Typer versions)
    result = runner.invoke(
        app,
        ["run", "--source", str(src), "--dest", str(dst), "--dry-run", "--verbose"],
    )

    # Debug dump on failure: show stdout and formatted exception/traceback
    if result.exit_code != 0:
        exc_text = ""
        if result.exception:
            exc_text = "".join(
                traceback.format_exception(
                    type(result.exception),
                    result.exception,
                    result.exception.__traceback__,
                )
            )
        debug = (
            f"\n--- STDOUT (merged stdout/stderr) ---\n{result.stdout}"
            f"\n--- EXCEPTION/TRACEBACK ---\n{exc_text or 'None'}\n"
        )
        pytest.fail(f"CLI failed with exit_code={result.exit_code}.{debug}")

    # Assert
    assert result.exit_code == 0
    assert "Completed successfully" in result.stdout


def test_cli_run_error_on_missing_source(tmp_path: Path):
    # The source doesn't exist
    src = tmp_path / "missing"
    dst = tmp_path / "dst"
    dst.mkdir()
    result = runner.invoke(
        app, ["run", "--source", str(src), "--dest", str(dst), "--dry-run"]
    )
    # The CLI catches the exception and exits with code 1
    assert result.exit_code == 1
    assert "Error:" in result.stdout
