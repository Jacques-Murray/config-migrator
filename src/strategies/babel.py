# Author: Jacques Murray
import json
from pathlib import Path
from typing import List
from src.core.interfaces import MigrationStrategy
from src.core.expections import ParsingError
from src.utils.fs_handler import FileSystemHandler
from src.utils.js_serializer import JSSerializer
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class BabelStrategy(MigrationStrategy):
    """
    Strategy to migrate .babelrc (JSON) to babel.config.js (ESM).
    """

    @property
    def name(self) -> str:
        return "Babel (.babelrc -> babel.config.js)"

    def detect(self, directory: Path) -> List[Path]:
        return list(directory.glob(".babelrc")) + list(directory.glob(".babelrc.json"))

    def migrate(self, file_path: Path) -> None:
        logger.info(f"Starting migration for {file_path} using {self.name}")

        try:
            content = FileSystemHandler.read_file(file_path)
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ParsingError(f"Failed to parse JSON from {file_path}: {e}")

        # Babel config structure is largely compatible, just needs to be wrapped in JS export
        new_filename = file_path.parent / "babel.config.js"
        js_content = JSSerializer.generate_esm_export(data)

        FileSystemHandler.write_file(new_filename, js_content)
        FileSystemHandler.delete_file(file_path)

        logger.info(f"Successfully migrated to {new_filename}")
