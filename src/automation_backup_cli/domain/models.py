# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional

# Single source of truth for compression choices
CompressionFormat = Literal["zip", "tar"] # type alias

@dataclass(frozen=True)
class BackupJob:
    """Parameters to execute a backup run. """
    source: str
    destination: str
    exclude_patterns: List[str] = field(default_factory=list)
    compress_format: Optional[CompressionFormat] = None  # "zip" | "tar" | None
    dry_run: bool = False


@dataclass
class BackupResult:
    files_planned: List[str] = field(default_factory=list)
    files_copied: List[str] = field(default_factory=list)
    compressed_artifact: Optional[str] = None
    errors: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class PlanItem:
    """Immutable plan row describing a single source->destination mapping."""
    source: str
    destination: str
    size_bytes: int

@dataclass
class PlanResult:
    """Aggregate result for a dry-run plan."""
    items: List[PlanItem] = field(default_factory=list)
    total_files: int = 0
    total_size_bytes: int = 0
