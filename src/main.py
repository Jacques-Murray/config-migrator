# Author: Jacques Murray
import typer
from pathlib import Path
from src.core.manager import MigrationManager
from src.utils.logger import setup_logger
from src.config import settings

app = typer.Typer(help="CLI tool to migrate legacy config files to modern formats.")
logger = setup_logger("cli")


@app.command()
def run(
    path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        help="The project root directory to scan.",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Simulate migration without writing files."
    ),
    verbose: bool = typer.Option(
        False, "--verbose", help="Enable verbose debug logging."
    ),
):
    """
    Scans the directory for legacy configuration files (ESLint, Babel)
    and migrates them to modern JS formats.
    """
    if verbose:
        settings.LOG_LEVEL = "DEBUG"

    # Note: Logic for dry_run would ideally be injected into FileSystemHandler.
    # For this implementation, we set it in global settings, though strict DI is preferred
    # in larger apps.
    settings.DRY_RUN = dry_run

    if dry_run:
        logger.warning("DRY RUN MODE: No files will be modified.")

    manager = MigrationManager()
    manager.scan_and_migrate(path)


if __name__ == "__main__":
    app()
