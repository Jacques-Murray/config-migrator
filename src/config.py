# Author: Jacques Murray
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application-wide configuration settings.
    """

    LOG_LEVEL: str = "INFO"
    DRY_RUN: bool = False
    BACKUP_EXTENSION: str = ".bak"

    class Config:
        env_prefix = "MIGRATOR_"
        case_sensitive = True


settings = Settings()
