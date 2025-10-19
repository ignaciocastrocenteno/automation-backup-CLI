# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Ignacio Castro Centeno

from __future__ import annotations
import typer
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .app import run_backup_job
from .domain.models import BackupJob
from .services.backup_service import build_backup_plan
from .utils.format import human_size

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

@app.command("plan")
def plan(
    source: str = typer.Option(..., "--source", "-s", help="Source directory"),
    destination: str = typer.Option(..., "--dest", "-d", help="Destination directory"),
    exclude: list[str] = typer.Option(
        [], "--exclude", "-e", help="Glob patterns to exclude (e.g. *.tmp, *.log)"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose logs"),
) -> None:
    """
    Show a dry-run plan as a table (no filesystem changes).
    """
    console.print(Panel.fit("automation-backup-cli — Plan", title="Preview"))
    try:
        # Construct a strongly-typed domain object (no **kwargs to please the type checker)
        job = BackupJob(
            source=source,
            destination=destination,
            exclude_patterns=exclude or [],
            compress_format=None,
            dry_run=True,
        )

        # Avoiding circular dependency references
        plan_result = build_backup_plan(job)

        table = Table(title="Planned copy", expand=True, show_lines=False)
        table.add_column("Source", overflow="fold")
        table.add_column("Destination", overflow="fold")
        table.add_column("Size", justify="right")

        for it in plan_result.items:
            table.add_row(it.source, it.destination, human_size(it.size_bytes))

        console.print(table)
        console.print(
            f"[bold]Total files:[/] {plan_result.total_files}   "
            f"[bold]Total size:[/] {human_size(plan_result.total_size_bytes)}"
        )
        return

    except typer.Exit:
        raise
    except Exception as exc:
        console.print(f"[bold red]Error:[/] {exc}")
        raise typer.Exit(code=1)
