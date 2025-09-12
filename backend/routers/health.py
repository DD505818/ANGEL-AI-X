"""Health check endpoints."""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class HealthStatus(BaseModel):
    """Schema for health check responses."""

    status: str


@router.get("/healthz", response_model=HealthStatus)
async def health() -> HealthStatus:
    """Liveness probe returning static status."""
    return HealthStatus(status="ok")
