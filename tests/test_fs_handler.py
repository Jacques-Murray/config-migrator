# Author: Jacques Murray
import pytest
from pathlib import Path
from src.utils.fs_handler import FileSystemHandler
from src.config import settings


def test_read_write_file(tmp_path: Path):
    """Verifies basic read/write operations."""
    test_file = tmp_path / "test.txt"
    content = "Hello World"

    FileSystemHandler.write_file(test_file, content)
    assert test_file.exists()
    assert FileSystemHandler.read_file(test_file) == content


def test_backup_creation_on_overwrite(tmp_path: Path):
    """Verifies a backup is created when overwriting an existing file."""
    test_file = tmp_path / "config.js"
    original_content = "old_config"
    new_content = "new_config"

    # Initial write
    test_file.write_text(original_content)

    # Overwrite using handler
    FileSystemHandler.write_file(test_file, new_content)

    # Check main file updated
    assert test_file.read_text(encoding="utf-8") == new_content

    # Check backup exists
    backup_file = test_file.with_suffix(test_file.suffix + settings.BACKUP_EXTENSION)
    assert backup_file.exists()
    assert backup_file.read_text(encoding="utf-8") == original_content


def test_delete_file_creates_backup(tmp_path: Path):
    """Verifies deleting a file actually keeps a backup."""
    test_file = tmp_path / "todelete.json"
    test_file.write_text("{}")

    FileSystemHandler.delete_file(test_file)

    assert not test_file.exists()
    backup_file = test_file.with_suffix(test_file.suffix + settings.BACKUP_EXTENSION)
    assert backup_file.exists()
