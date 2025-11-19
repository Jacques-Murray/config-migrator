# Author: Jacques Murray
import json
from pathlib import Path
from typing import List, Dict, Any
from src.core.interfaces import MigrationStrategy
from src.core.expections import ParsingError
from src.utils.fs_handler import FileSystemHandler
from src.utils.js_serializer import JSSerializer
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ESLintStrategy(MigrationStrategy):
    """
    Strategy to migrate legacy .eslintrc (JSON) to eslint.config.js (Flat Config).
    """

    @property
    def name(self) -> str:
        return "ESLint (Legacy JSON -> Flat Config)"

    def detect(self, directory: Path) -> List[Path]:
        # We focus on JSON for safety in parsing.
        # JS-based legacy configs are harder to parse reliably in Python without a JS runtime.
        return list(directory.glob(".eslintrc.json")) + list(
            directory.glob(".eslintrc")
        )

    def migrate(self, file_path: Path) -> None:
        logger.info(f"Starting migration for {file_path} using {self.name}")

        try:
            content = FileSystemHandler.read_file(file_path)
            # Handle cases where .eslintrc is JSON but missing extension
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ParsingError(f"Failed to parse JSON from {file_path}: {e}")

        transformed_data = self._transform_to_flat_config(data)

        new_filename = file_path.parent / "eslint.config.js"
        js_content = JSSerializer.generate_esm_export(transformed_data)

        # Write new file
        FileSystemHandler.write_file(new_filename, js_content)

        # Remove old file (safely)
        FileSystemHandler.delete_file(file_path)

        logger.info(f"Successfully migrated to {new_filename}")

    def _transform_to_flat_config(
        self, old_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Transforms legacy Object-based config to Flat Config (Array or Objects).
        """
        flat_config = []

        # Base configuration object
        base_obj = {}

        # Map 'rules'
        if "rules" in old_config:
            base_obj["rules"] = old_config["rules"]

        # Map 'env' -> languageOptions.globals (Rough approximation)
        if "env" in old_config:
            # In a real scenario, we would map 'browser: true' to the 'globals' package imports
            # For now, we keep the structure generic or add a comment via documentation
            logger.warning("Migration of 'env' requires manual review in Flat Config.")
            base_obj["languageOptions"] = {"globals": old_config["env"]}

        # Map 'parserOptions' => languageOptions
        if "parserOptions" in old_config:
            if "languageOptions" not in base_obj:
                base_obj["languageOptions"] = {}
            base_obj["languageOptions"].update(old_config["parserOptions"])

        # Map 'extends' -> This is complex in Flat Config.
        # In Flat Config, 'extends' are imported modules spread into the array.
        # Since we are generating text, we can't import modules dynamically easily.
        # We will put the extends strings in a custom field for the user to fix manually.
        if "extends" in old_config:
            logger.warning(
                "Migration of 'extends' requires manual import setup in eslint.config.js."
            )
            # We add a dummy rule/note so the user sees it
            flat_config.append({"ignores": ["**/*.config.js"]})  # Good practice default

        flat_config.append(base_obj)
        return flat_config
