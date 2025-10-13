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
    """
    CLI entry. Follows PEP8 naming and Typer best practices.
    """


@app.command("run")
def run(
    source: str = typer.Option(..., "--source", "-s", help="Source directory"),
    destination: str = typer.Option(..., "--dest", "-d", help="Destination directory"),
    exclude: Optional[List[str]] = typer.Option(
        None, "--exclude", "-e", help="Glob patterns to exclude (e.g. *.tmp, *.log)"
    ),
    compress: Optional[str] = typer.Option(
        None,
        "--compress",
        "-c",
        help="Compression format (zip or tar). If omitted, files are just copied.",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Simulate actions without copying/compressing."
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output (INFO level)."
    ),
) -> None:
    """
    Execute a backup job. Use --dry-run to preview actions (Pythonic safety).
    """
    console.print(Panel.fit("automation-backup-cli", title="Starting"))

    try:
        result = run_backup_job(
            source=source,
            destination=destination,
            exclude_patterns=exclude or [],
            compress_format=compress,
            dry_run=dry_run,
            verbose=verbose,
        )
        if result.errors:
            console.print(f"[bold red]Completed with {len(result.errors)} errors[/]")
            raise typer.Exit(code=2)
        else:
            console.print("[bold green]Completed successfully[/]")
            raise typer.Exit(code=0)
    except Exception as exc:  # domain exceptions are raised from app/service
        console.print(f"[bold red]Error:[/] {exc}")
        raise typer.Exit(code=1)
