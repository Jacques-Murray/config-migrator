# Author: Jacques Murray


class MigrationError(Exception):
    """Base class for migration exceptions."""

    pass


class StrategyNotFoundError(MigrationError):
    """Raised when no strategy is found for a file."""

    pass


class ParsingError(MigrationError):
    """Raised when a legacy config file cannot be parsed."""

    pass
