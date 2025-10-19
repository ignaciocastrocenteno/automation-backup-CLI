# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno

from __future__ import annotations

import runpy
import sys
import pytest

def test_main_module_help_exits_zero():
    """
    Execute `python -m automation_backup_cli --help` and ensure it exits with code 0.
    This covers the __main__.py entrypoint.
    """
    argv_backup = sys.argv[:]
    try:
        sys.argv = ["python", "--help"]
        with pytest.raises(SystemExit) as excinfo:
            runpy.run_module("automation_backup_cli", run_name="__main__")
        assert excinfo.value.code == 0
    finally:
        sys.argv = argv_backup
