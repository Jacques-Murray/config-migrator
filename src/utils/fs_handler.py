# Author: Jacques Murray
import shutil
import os
from pathlib import Path
from typing import Optional
from src.utils.logger import setup_logger
from src.config import settings

logger = setup_logger(__name__)


class FileSystemHandler:
    """
    Handles file system operations with built-in safety mechanisms (backups).
    """

    @staticmethod
    def create_backup(file_path: Path) -> Path:
        """
        Creates a backup of the specified file.

        Args:
          file_path (Path): The file to back up.

        Returns:
          Path: The path to the backup file.
        """
        backup_path = file_path.with_suffix(
            file_path.suffix + settings.BACKUP_EXTENSION
        )
        try:
            shutil.copy2(file_path, backup_path)
            logger.debug(f"Backup created: {backup_path}")
            return backup_path
        except OSError as e:
            logger.error(f"Failed to create backup for {file_path}: {e}")
            raise

    @staticmethod
    def read_file(file_path: Path) -> str:
        """Reads file content safely."""
        try:
            return file_path.read_text(encoding="utf-8")
        except OSError as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise

    @staticmethod
    def write_file(file_path: Path, content: str) -> None:
        """
        Writes content to file. If file exists, creates a backup first.

        Args:
          file_path (Path): Target path.
          content (str): Content to write.
        """
        if file_path.exists():
            FileSystemHandler.create_backup(file_path)

        try:
            file_path.write_text(content, encoding="utf-8")
            logger.info(f"[green]Successfully wrote to {file_path}[/green]")
        except OSError as e:
            logger.error(f"Error writing file {file_path}: {e}")
            raise

    @staticmethod
    def delete_file(file_path: Path) -> None:
        """Deletes a file safely, ensuring a backup exists if needed."""
        # In the migration utility, we usually keep the old file as backup
        # but specifically rename it.
        try:
            if file_path.exists():
                backup = FileSystemHandler.create_backup(file_path)
                os.remove(file_path)
                logger.info(f"Removed legacy file {file_path} (Backup at {backup})")
        except OSError as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            raise
