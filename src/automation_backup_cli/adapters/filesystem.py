# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

from pathlib import Path
from fnmatch import fnmatch
from typing import Iterable, List


def validate_directory(path: str) -> Path:
    p = Path(path).expanduser().resolve()
    if not p.exists() or not p.is_dir():
        raise FileNotFoundError(f"Directory not found: {p}")
    return p


def collect_files(source: Path, exclude_patterns: Iterable[str]) -> List[Path]:
    files: List[Path] = []
    for p in source.rglob("*"):
        if p.is_file():
            if any(fnmatch(p.name, pat) for pat in exclude_patterns):
                continue
            files.append(p)
    return files


def ensure_destination(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
