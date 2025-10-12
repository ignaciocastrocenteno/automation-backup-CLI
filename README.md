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
```

## License

Copyright (c) 2025 Ignacio Castro Centeno

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/
.

SPDX-License-Identifier: GPL-3.0-or-later
See the LICENSE
 file for details.
