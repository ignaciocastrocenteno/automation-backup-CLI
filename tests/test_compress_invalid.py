# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

import pytest
from pathlib import Path
from automation_backup_cli.domain.models import BackupJob
from automation_backup_cli.services.backup_service import execute_backup


def test_execute_backup_invalid_compress_format_raises(tmp_path: Path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    (src / "f.txt").write_text("A")
    dst.mkdir()

    job = BackupJob(
        source=str(src),
        destination=str(dst),
        exclude_patterns=[],
        compress_format="rar",  # not supported
        dry_run=False,
    )

    with pytest.raises(ValueError):
        execute_backup(job)
