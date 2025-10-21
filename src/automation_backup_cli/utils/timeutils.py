# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

from datetime import datetime


def dated_subfolder() -> str:
    """Return a folder path like 'YYYY/MM/DD' (string)."""
    now = datetime.now()
    return f"{now:%Y}/{now:%m}/{now:%d}"
