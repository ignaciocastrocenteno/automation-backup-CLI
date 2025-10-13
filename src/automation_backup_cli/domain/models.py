# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class BackupJob:
    source: str
    destination: str
    exclude_patterns: List[str] = field(default_factory=list)
    compress_format: Optional[str] = None  # "zip" | "tar" | None
    dry_run: bool = True


@dataclass
class BackupResult:
    files_planned: List[str] = field(default_factory=list)
    files_copied: List[str] = field(default_factory=list)
    compressed_artifact: Optional[str] = None
    errors: List[str] = field(default_factory=list)
