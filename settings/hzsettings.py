import os

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "HypeZone"
    DEBUG: bool = True
    ALCHEMY_DB_URL: str = os.getenv("ALCHEMY_DB_URL", "")
    JWT_SHARED_SECRET: str = os.getenv("JWT_SHARED_SECRET", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRES_IN: int = os.getenv("JWT_EXPIRES_IN", 3600)

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
