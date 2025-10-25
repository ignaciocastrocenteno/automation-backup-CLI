# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

from datetime import date
from pathlib import Path
import re
import shutil
from typing import List

# Strict patterns for YYYY / MM / DD
_YEAR = re.compile(r"^\d{4}$")
_MON = re.compile(r"^(0[1-9]|1[0-2])$")
_DAY = re.compile(r"^(0[1-9]|[12]\d|3[01])$")


def _is_dated_triplet(path: Path, root: Path) -> bool:
    """
    Ensure path is root/YYYY/MM/DD and all parts exist.
    Prevents accidental deletions outside the expected structure.
    """
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    parts = rel.parts
    return (
        len(parts) == 3
        and _YEAR.fullmatch(parts[0]) is not None
        and _MON.fullmatch(parts[1]) is not None
        and _DAY.fullmatch(parts[2]) is not None
    )


def _date_of_triplet(path: Path) -> date:
    y, m, d = path.parts[-3:]
    return date(int(y), int(m), int(d))


def purge_old_backups(
    destination_root: Path, cutoff: date, dry_run: bool = False
) -> List[Path]:
    """
    Delete dated folders under destination_root older than `cutoff`.
    Returns the list of directories scheduled/removed (absolute Paths).
    Only directories matching YYYY/MM/DD are considered.
    """
    removed: List[Path] = []
    if not destination_root.exists():
        return removed

    # Walk only 3 levels deep: YYYY/MM/DD
    for ydir in destination_root.iterdir():
        if not (ydir.is_dir() and _YEAR.match(ydir.name)):
            continue
        for mdir in ydir.iterdir():
            if not (mdir.is_dir() and _MON.match(mdir.name)):
                continue
            for ddir in mdir.iterdir():
                if not (ddir.is_dir() and _DAY.match(ddir.name)):
                    continue
                if not _is_dated_triplet(ddir, destination_root):
                    continue
                d = _date_of_triplet(ddir)
                if d < cutoff:
                    removed.append(ddir.resolve())
                    if not dry_run:
                        shutil.rmtree(ddir, ignore_errors=False)

            # Clean up empty month dirs
            if not any(mdir.iterdir()):
                if not dry_run:
                    mdir.rmdir()
        # Clean up empty year dirs
        if not any(ydir.iterdir()):
            if not dry_run:
                ydir.rmdir()
    return removed
