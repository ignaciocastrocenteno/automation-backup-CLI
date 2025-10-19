# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno

from __future__ import annotations

from automation_backup_cli.utils.format import human_size

def test_human_size_binary_units_until_pib():
    """
    Cover the final branch in human_size() by passing a very large number.
    """
    assert human_size(0) == "0 B"
    assert human_size(1023) == "1023 B"
    assert human_size(1024) == "1 KiB"
    assert human_size(1024**2) == "1 MiB"
    assert human_size(1024**3) == "1 GiB"
    assert human_size(1024**4) == "1 TiB"
    # Force the loop to fall through and return the PiB line
    assert human_size(1024**5) == "1 PiB"
