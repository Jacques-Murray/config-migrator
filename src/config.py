# Author: Jacques Murray
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application-wide configuration settings.
    """

    LOG_LEVEL: str = "INFO"
    DRY_RUN: bool = False
    BACKUP_EXTENSION: str = ".bak"

    # Pydantic V2 Configuration
    model_config = SettingsConfigDict(env_prefix="MIGRATOR_", case_sensitive=True)


settings = Settings()
