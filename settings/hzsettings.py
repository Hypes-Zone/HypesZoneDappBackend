import os

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "HypeZone"
    DEBUG: bool = True
    ALCHEMY_DB_URL: str = os.getenv("ALCHEMY_DB_URL", "")
    SHARED_SECRET: str = os.getenv("SHARED_SECRET", "")

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
