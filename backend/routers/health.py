"""Health check endpoints."""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def health() -> dict[str, str]:
    """Liveness probe returning static status."""
    return {"status": "ok"}
