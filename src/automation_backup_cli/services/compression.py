# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

from pathlib import Path
import shutil
from typing import Optional


def compress_folder(folder: Path, fmt: Optional[str]) -> Optional[Path]:
    """
    Compress 'folder' into zip or tar, returns the artifact path.
    If fmt is None, do nothing and return None.
    """
    if not fmt:
        return None
    fmt = fmt.lower().strip()
    if fmt not in {"zip", "tar"}:
        raise ValueError("compress format must be 'zip' or 'tar'")

    base_name = folder.as_posix()
    # shutil.make_archive returns the filename (str) without extension param repetition.
    artifact = shutil.make_archive(base_name, fmt, root_dir=folder)
    return Path(artifact).resolve()
