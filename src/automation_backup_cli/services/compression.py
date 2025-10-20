# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

from pathlib import Path
from shutil import make_archive
from typing import Literal

# We support two formats:
# - "zip"  -> .zip
# - "tar"  -> .tar.gz (gztar)
from ..domain.models import CompressionFormat

def create_archive(
    destination_root: Path,
    dated_subdir: Path,
    timestamp: str,
    fmt: CompressionFormat,
) -> Path:
    """
    Create an archive for the dated backup directory.

    The archive will be placed at:
      destination_root / f"backup_{timestamp}.zip or .tar.gz"

    The internal paths will preserve YYYY/MM/DD/... by archiving
    relative to the destination_root, not to YYYY/MM.
    """
    if fmt not in ("zip", "tar"):
        raise ValueError("Unsupported compression format: use 'zip' or 'tar'.")

    archive_base = destination_root / f"backup_{timestamp}"

    # Include full YYYY/MM/DD in the archive:
    #   root_dir = destination_root
    #   base_dir = relative path from destination_root to dated_subdir ("YYYY/MM/DD")
    rel = dated_subdir.relative_to(destination_root)
    root_dir = destination_root
    base_dir = str(rel)  # e.g., "2025/10/14" (OS separator handled by shutil)

    shutil_fmt = "zip" if fmt == "zip" else "gztar"

    archive_path = make_archive(
        base_name=str(archive_base),
        format=shutil_fmt,
        root_dir=str(root_dir),
        base_dir=base_dir,
    )
    return Path(archive_path).resolve()
