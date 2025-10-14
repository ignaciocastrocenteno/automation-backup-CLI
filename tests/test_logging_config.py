# tests/test_logging_config.py
from __future__ import annotations
import logging
from automation_backup_cli.adapters.logging_config import setup_logging
from rich.logging import RichHandler

def test_setup_logging_verbose_true_sets_info_level():
    setup_logging(verbose=True)
    root = logging.getLogger()
    assert root.level == logging.INFO
    assert any(isinstance(h, RichHandler) for h in root.handlers)

def test_setup_logging_verbose_false_sets_warning_level():
    setup_logging(verbose=False)
    root = logging.getLogger()
    assert root.level == logging.WARNING
    assert any(isinstance(h, RichHandler) for h in root.handlers)
