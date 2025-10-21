# automation-backup-cli

A Python CLI to **plan and run** backups from a source directory to a destination, with:
- date-based organization (folders `YYYY/MM/DD`),
- exclusion patterns (glob),
- **dry-run** preview (no filesystem changes),
- optional **compression** (`zip` or `tar.gz`),
- friendly terminal output via **Rich**.

> Goal: showcase professional-grade Python engineering for recruiters and reviewers (clean architecture, tests, typing, docs).

---

## Features

- **Plan mode**: preview exactly *what would be copied* with a Rich table (no changes on disk).
- **Dry-run**: simulate the full run; collect planned targets and print informative logs.
- **Copy**: mirror files from source into a dated structure `YYYY/MM/DD/...`.
- **Exclude patterns**: ignore paths by glob (e.g. `*.tmp`, `*.log`, `**/__pycache__/*`).
- **Compression**: `--compress zip` or `--compress tar` ⇒ produces `backup_<YYYYMMDD>_<HHMMSS>.(zip|tar.gz)` at the destination root, preserving `YYYY/MM/DD` inside the archive.
- **Logging**: Rich-styled messages, clear success/errors, consistent exit codes.

**Planned (next sprints)**
- `--retention-days N`: purge dated folders older than `N` days.
- Config file (`.toml/.yaml`) with precedence: CLI > ENV > file.
- File logging with rotation.
- CI and packaging guidance.

## Tech Stack

- Python **3.10+**
- **Typer** (CLI), **Rich** (console)
- **pytest**, **pytest-cov**, **freezegun** (tests)
- **ruff**, **black**, (pre-commit optional)
- Packaging via `uv` (or `pip`, `pipx`)

## Installation / Development

### Using `uv` (recommended for dev)

```bash
# Sync dependencies (creates a local venv)
uv sync

# Run tests
uv run pytest -q
```

## Run the CLI (3 ways)
```bash
### 1) Within uv-managed venv (entry point script)
uv run automation-backup --help

### 2) As Python module (thanks to __main__.py)
uv run python -m automation_backup_cli --help

### 3) (Optional) Install in editable mode for development
uv pip install -e .
automation-backup --help
```

## Usage
```bash
### 1) Preview (no changes): plan
uv run automation-backup plan \
  --source /path/to/src \
  --dest   /path/to/dst \
  --exclude "*.tmp" --exclude "**/__pycache__/*"

### Output example (Rich Table):
┏━━━━━━━━━━━━━━━━━━━━━━━ Planned copy ━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Source                         Destination             Size ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ /src/dir/a.txt                /dst/2025/10/14/dir/a.txt  1B │
└─────────────────────────────────────────────────────────────┘
Total files: 1  Total size: 1 B

### 2) Dry-run (simulate a real run)
uv run automation-backup run \
  --source /path/to/src \
  --dest   /path/to/dst \
  --exclude "*.log" \
  --dry-run --verbose

### 3) Real copy + optional compression
# Copy only
uv run automation-backup run --source /src --dest /dst

# Copy and zip
uv run automation-backup run --source /src --dest /dst --compress zip

# Copy and tar.gz
uv run automation-backup run --source /src --dest /dst --compress tar
```

The compressed artifact will be created at the destination root as:
/dst/backup_<YYYYMMDD>_<HHMMSS>.zip
### or
/dst/backup_<YYYYMMDD>_<HHMMSS>.tar.gz

and it preserves YYYY/MM/DD/... structure inside the archive.

## Exit Codes
- 0 — Success (no errors)
- 1 — Unexpected error (exception path)
- 2 — Partial failure (completed with collected errors)

## Exclude Patterns (glob)
- Use multiple -e/--exclude options:
    --exclude "*.tmp"
    --exclude "**/__pycache__/*"
- Patterns are applied against paths under the source.

## Project Structure
```bash
src/automation_backup_cli/
  __main__.py         # module entrypoint: python -m automation_backup_cli
  cli.py              # Typer CLI: run, plan
  app.py              # Orchestration (run_backup_job)
  services/
    backup_service.py # plan + execute + compression integration
    compression.py    # create_archive(zip/tar.gz), timestamped artifact
  adapters/
    filesystem.py     # validate, collect_files, ensure_destination
    logging_config.py # Rich logging (console)
  domain/
    models.py         # dataclasses + type aliases (CompressionFormat)
    exceptions.py     # domain-specific errors
  utils/
    timeutils.py      # dated_subfolder (YYYY/MM/DD)
    format.py         # human_size
tests/ ...            # 100% coverage across features
```

## Development
### Tests
```bash
uv run pytest -q
uv run pytest --cov=src --cov-report=term-missing
```

### Lint & Font (if enabled)
```bash
ruff check .
black .
```

### Type checking (optional)
If using pyright/basedpyright in your editor, types are kept consistent across domain/CLI/services.

## Roadmap
- ```bash --retention-days N``` (purge old dated folders)
- Config file (.toml/.yaml) and precedence resolution
- File logging with rotation
- GitHub Actions: CI matrix (Windows/macOS/Linux), build/test; optional release draft
- Packaging (sdist/wheel) and pipx installation instructions

## License
GPL-3.0-or-later
Copyright (c) 2025 Ignacio Castro Centeno

See the LICENSE file for full terms.
