# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

import logging
from rich.logging import RichHandler


# Update: logging.basicConfig didn't use to reconfigure the login whether
# there was previously another process that had configured logging before
#  (e.g. a test suite)
def setup_logging(verbose: bool = False) -> None:
    """
    Configure root logger with RichHandler.
    Use `force=True` so tests (and repeated runs) actually reconfigure logging.
    """
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)],
        force=True,  # <- key to make tests deterministic
    )
