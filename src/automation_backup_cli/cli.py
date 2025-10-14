# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno
from __future__ import annotations

import typer
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel
from .app import run_backup_job

app = typer.Typer(help="automation-backup-cli: organize and backup files safely.")
console = Console()

@app.callback()
def main_callback() -> None:
    """CLI entrypoint (Typer)."""

@app.command("run")
def run(
    source: str = typer.Option(..., "--source", "-s", help="Source directory"),
    destination: str = typer.Option(..., "--dest", "-d", help="Destination directory"),
    exclude: list[str] = typer.Option(
        [], "--exclude", "-e", help="Glob patterns to exclude (e.g. *.tmp, *.log)"
    ),
    compress: str | None = typer.Option(
        None, "--compress", "-c", help="Compression format: zip or tar"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate actions only"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose logs"),
) -> None:
    """Run the backup job."""
    console.print(Panel.fit("automation-backup-cli", title="Starting"))

    try:
        result = run_backup_job(
            source=source,
            destination=destination,
            exclude_patterns=exclude,
            compress_format=compress,
            dry_run=dry_run,
            verbose=verbose,
        )
        if result.errors:
            console.print(f"[bold red]Completed with {len(result.errors)} errors[/]")
            # Non-zero exit for partial failures
            raise typer.Exit(code=2)

        console.print("[bold green]Completed successfully[/]")
        # Success path: just return (exit code 0)
        return

    except typer.Exit:
        # Preserve explicit exit codes (do not convert success into failure).
        raise
    except Exception as exc:
        console.print(f"[bold red]Error:[/] {exc}")
        # Generic failure
        raise typer.Exit(code=1)
