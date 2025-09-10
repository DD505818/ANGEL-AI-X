from pydantic import BaseModel
import os
class Settings(BaseModel):
    nats_url: str = os.getenv("NATS_URL","nats://localhost:4222")
    redis_url: str = os.getenv("REDIS_URL","redis://localhost:6379/0")
    ed25519_pubkey: str = os.getenv("ED25519_PUBKEY","")
    jwt_secret: str = os.getenv("JWT_SECRET","dev")
    allow_origins: list[str] = os.getenv("ALLOW_ORIGINS","http://localhost:3000").split(",")
settings = Settings()
