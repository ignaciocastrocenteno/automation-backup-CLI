# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations


def human_size(num: int) -> str:
    """Return a human-readable size (binary units)."""
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if num < 1024:
            return f"{num} {unit}"
        num //= 1024
    return f"{num} PiB"
