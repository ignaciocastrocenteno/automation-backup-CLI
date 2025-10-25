# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

from pathlib import Path
from datetime import date
from freezegun import freeze_time

from automation_backup_cli.services.retention import purge_old_backups


def _mk_dated(dst: Path, y: int, m: int, d: int) -> Path:
    p = dst / f"{y:04d}" / f"{m:02d}" / f"{d:02d}"
    # Creating a dated structure
    p.mkdir(parents=True, exist_ok=True)
    (p / "keep.txt").write_text("x", encoding="utf-8")
    return p


@freeze_time("2025-10-14")
def test_purge_old_backups_deletes_older_than_cutoff(tmp_path: Path):
    dst = tmp_path / "dst"
    dst.mkdir()
    # Create dated dirs around the cutoff
    old1 = _mk_dated(dst, 2025, 10, 10)
    old2 = _mk_dated(dst, 2025, 10, 12)
    keep = _mk_dated(dst, 2025, 10, 14)

    cutoff = date(2025, 10, 13)  # remove strictly older than 2025-10-13
    removed = purge_old_backups(dst, cutoff, dry_run=False)

    assert old1 not in removed or old1.exists() is False
    assert old2 not in removed or old2.exists() is False
    assert keep.exists()
    assert all(p.exists() is False for p in removed)


@freeze_time("2025-10-14")
def test_purge_old_backups_dry_run_does_not_delete(tmp_path: Path):
    dst = tmp_path / "dst"
    dst.mkdir()
    old1 = _mk_dated(dst, 2025, 9, 30)  # Zero-padding error corrected
    cutoff = date(2025, 10, 10)
    removed = purge_old_backups(dst, cutoff, dry_run=True)

    assert old1 in removed
    assert old1.exists()


def test_purge_old_backups_ignores_non_dated(tmp_path: Path):
    dst = tmp_path / "dst"
    dst.mkdir()
    weird = dst / "notadate"
    (weird / "foo").mkdir(parents=True)
    cutoff = date(2025, 1, 1)
    removed = purge_old_backups(dst, cutoff, dry_run=False)

    assert removed == []
    assert weird.exists()
