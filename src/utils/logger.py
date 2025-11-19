# Author: Jacques Murray
import logging
from rich.logging import RichHandler
from src.config import settings


def setup_logger(name: str) -> logging.Logger:
    """
    Configures and returns a structured logger using RichHandler.

    Args:
      name (str): The name of the logger context.

    Returns:
      logging.Logger: Configured logger instance.
    """
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="$(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)],
    )
    return logging.getLogger(name)
