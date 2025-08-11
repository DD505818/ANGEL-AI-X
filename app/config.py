"""Application configuration via environment variables."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Strongly typed application settings."""

    postgres_url: str = Field(alias="POSTGRES_URL")
    redis_url: str = Field(alias="REDIS_URL")
    jwt_secret: str = Field(alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=15, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    totp_issuer: str = Field(default="ANGEL.AI", alias="TOTP_ISSUER")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, populate_by_name=True)


settings = Settings()
