# Author: Jacques Murray
from pathlib import Path
from typing import List
from src.core.interfaces import MigrationStrategy
from src.strategies.eslint import ESLintStrategy
from src.strategies.babel import BabelStrategy
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class MigrationManager:
    """
    Orchestrates the registration and execution of migration strategies.
    """

    def __init__(self):
        self.strategies: List[MigrationStrategy] = []
        self._register_defaults()

    def _register_defaults(self):
        self.strategies.append(ESLintStrategy())
        self.strategies.append(BabelStrategy())

    def scan_and_migrate(self, target_dir: Path) -> None:
        """
        Runs all strategies against the target directory.
        """
        logger.info(f"Scanning directory: {target_dir}")

        found_any = False

        for strategy in self.strategies:
            detected_files = strategy.detect(target_dir)
            if detected_files:
                found_any = True
                logger.info(
                    f"Strategy '{strategy.name}' detected {len(detected_files)} file(s)."
                )
                for file_path in detected_files:
                    try:
                        strategy.migrate(file_path)
                    except Exception as e:
                        logger.error(f"Failed to migrate {file_path}: {e}")

        if not found_any:
            logger.info("No legacy configuration files detected.")
