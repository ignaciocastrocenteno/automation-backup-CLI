# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno

from __future__ import annotations
import pytest
from automation_backup_cli.adapters.filesystem import validate_directory

def test_validate_directory_raises_when_missing(tmp_path):
    missing = tmp_path / "nope"
    with pytest.raises(FileNotFoundError):
        validate_directory(str(missing))
