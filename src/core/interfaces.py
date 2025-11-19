# Author: Jacques Murray
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class MigrationStrategy(ABC):
    """
    Abstract Base Class defining the contract for specific migration strategies.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the name of the strategy."""
        pass

    @abstractmethod
    def detect(self, directory: Path) -> List[Path]:
        """
        Scans the directory for files applicable to this strategy.

        Args:
          directory (Path): The root directory to scan.

        Returns:
          List[Path]: A list of detected legacy file paths.
        """
        pass

    @abstractmethod
    def migrate(self, file_path: Path) -> None:
        """
        Performs the migration logic on a specific file.

        Args:
          file_path (Path): The file to migrate.
        """
        pass
