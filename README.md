# automation-backup-cli

A Python CLI to **simulate and run** backups from a source directory to a destination,
with date-based organization, optional compression, exclusion patterns, and **dry-run** mode.

## Features (MVP)
- Dry-run (simulate without changing files)
- Copy from source to destination
- Date-based folders (YYYY/MM/DD)
- Exclude by glob patterns
- Optional compression (zip/tar) [coming soon]
- Logging with Rich

## Tech Stack
- Python 3.10+
- Typer (CLI)
- Rich (nice terminal output)
- Pytest + pytest-cov + freezegun (tests)

## Install (dev)
```bash
uv sync
uv run pytest
