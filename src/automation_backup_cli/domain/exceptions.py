# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
class BackupError(Exception):
    """Generic backup error."""


class InvalidPathError(BackupError):
    """Raised when a provided path is invalid or not accessible."""


class CompressionError(BackupError):
    """Raised when compression fails."""
