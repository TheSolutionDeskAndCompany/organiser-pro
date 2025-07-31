from typing import Optional
import platform
import sys

import click
from rich.console import Console

from .commands import sort_by_type, sort_by_date, dedupe

# Initialize console for rich output
console = Console()
VERSION = "0.1.0"


def check_os_compatibility():
    """Check if running on supported OS and warn if not."""
    if platform.system() != "Linux":
        console.print(
            f"[bold red]⚠️  Warning: OrganiserPro Linux Edition[/bold red]\n"
            f"This version is designed for Linux desktop environments only.\n"
            f"Detected OS: {platform.system()}\n\n"
            f"[yellow]Windows and Mac support are planned for future releases.[/yellow]\n"
            f"For the best experience, please use the GUI version: [bold]organiserpro-gui[/bold]\n"
            f"Visit our GitHub for updates on cross-platform support.\n"
        )
        if platform.system() in ["Windows", "Darwin"]:
            console.print("[red]Exiting due to unsupported platform.[/red]")
            sys.exit(1)


# Create the main CLI group
@click.group(
    name="organiserpro",
    invoke_without_command=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(version=VERSION, message="%(prog)s, version %(version)s")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """OrganiserPro CLI - Linux Edition (Advanced/Developer Interface)"""
    # Check OS compatibility
    check_os_compatibility()
    
    if ctx.invoked_subcommand is None:
        console.print("[bold blue]OrganiserPro CLI - Linux Edition[/bold blue]")
        console.print("[yellow]Advanced/Developer Interface[/yellow]\n")
        console.print("[dim]For regular users, we recommend the GUI version:[/dim]")
        console.print("[bold green]organiserpro-gui[/bold green]\n")
        console.print("[bold]Available CLI Commands:[/bold]")
        console.print("  [cyan]sort-by-type[/cyan]    Sort files in DIRECTORY by file type")
        console.print("  [cyan]sort-by-date[/cyan]    Sort files in DIRECTORY by date")
        console.print("  [cyan]dedupe[/cyan]          Find and handle duplicate files in DIRECTORY")
        console.print(
            "\n[dim]Use 'organiserpro-cli COMMAND --help' for more information about a command.[/dim]"
        )
        ctx.exit(0)


# Register all commands with the main CLI
cli.add_command(sort_by_type)
cli.add_command(sort_by_date)
cli.add_command(dedupe)


# Keep these functions for backward compatibility with tests
def sort_by_type_cmd(directory: str, dry_run: bool = False) -> int:
    """Legacy function for sort by type functionality."""
    from .commands import sort_by_type_impl

    # Call the implementation directly
    sort_by_type_impl(directory=directory, dry_run=dry_run)
    return 0


def sort_by_date_cmd(directory: str, date_format: str, dry_run: bool = False) -> int:
    """Legacy function for sort by date functionality."""
    from .sorter import sort_by_date as sort_by_date_impl

    # Call the implementation directly
    sort_by_date_impl(directory=directory, date_format=date_format, dry_run=dry_run)
    return 0


def sort_by_size_cmd(directory: str, dry_run: bool = False) -> int:
    """Legacy function for sort by size functionality."""
    console.print(f"[bold]Sorting files in:[/] {directory}")
    console.print("[bold]Sort by:[/] size")

    if dry_run:
        console.print("[yellow]Dry run: No changes will be made")
        console.print("Would sort files by size")
    else:
        console.print("Sorting by size is not yet implemented", style="yellow")
    return 0


# Legacy function for backwards compatibility with tests
def dedupe_cmd(
    directory: str,
    recursive: bool = True,
    delete: bool = False,
    move_to: Optional[str] = None,
    dry_run: bool = False,
) -> int:
    """Legacy function for dedupe functionality."""
    from .dedupe import find_duplicates_cli

    # Call the implementation directly
    find_duplicates_cli(
        directory=directory,
        recursive=recursive,
        delete=delete,
        move_to=move_to,
        dry_run=dry_run,
    )
    return 0


if __name__ == "__main__":
    cli()
