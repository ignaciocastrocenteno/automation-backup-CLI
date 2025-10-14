# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

from pathlib import Path
import pytest
from typer.testing import CliRunner

# IMPORTANT: patch the symbol used by the CLI module, not the app module
from automation_backup_cli import cli as cli_module
from automation_backup_cli.domain.models import BackupResult

runner = CliRunner()


def test_cli_run_partial_failure_exit_2(monkeypatch, tmp_path: Path):
    """Simulate a run that finishes with domain-level errors (Exit code 2)."""

    def fake_run_backup_job(*args, **kwargs):
        br = BackupResult()
        br.errors = ["E1", "E2"]
        return br

    # Patch the symbol that the CLI actually calls
    monkeypatch.setattr(cli_module, "run_backup_job", fake_run_backup_job)

    src = tmp_path / "src"
    dst = tmp_path / "dst"
    (src / "a").mkdir(parents=True)
    (src / "a" / "file.txt").write_text("ok")
    dst.mkdir()

    result = runner.invoke(
        cli_module.app,
        ["run", "--source", str(src), "--dest", str(dst), "--dry-run"],
    )

    assert result.exit_code == 2
    assert "Completed with 2 errors" in result.stdout


def test_cli_run_unexpected_exception_exit_1(monkeypatch, tmp_path: Path):
    """Simulate an unexpected exception in the application layer (Exit code 1)."""

    def fake_run_backup_job(*args, **kwargs):
        raise RuntimeError("boom")

    # Patch the symbol that the CLI actually calls
    monkeypatch.setattr(cli_module, "run_backup_job", fake_run_backup_job)

    src = tmp_path / "src"
    dst = tmp_path / "dst"
    (src / "a").mkdir(parents=True)
    (src / "a" / "file.txt").write_text("ok")
    dst.mkdir()

    result = runner.invoke(
        cli_module.app,
        ["run", "--source", str(src), "--dest", str(dst), "--dry-run", "--verbose"],
    )

    assert result.exit_code == 1
    assert "Error:" in result.stdout
    # Optional: echo of the error message may or may not be present depending on how console prints it
    # assert "boom" in result.stdout
