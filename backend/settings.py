"""Application configuration settings using Pydantic BaseSettings."""
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Container for environment configuration.

    Environment variables are loaded from a `.env` file during development.
    Secrets must be provided by the runtime environment in production.
    """

    env: str = "production"
    jwt_secret: str
    admin_ips: List[str] = ["10.0.0.5", "203.0.113.7"]
    redis_url: str
    nats_url: Optional[str] = None
    pg_dsn: str

    # venue API credentials
    binance_key: Optional[str] = None
    binance_secret: Optional[str] = None
    kraken_key: Optional[str] = None
    kraken_secret: Optional[str] = None
    bybit_key: Optional[str] = None
    bybit_secret: Optional[str] = None
    okx_key: Optional[str] = None
    okx_secret: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")  # development only


settings = Settings()
