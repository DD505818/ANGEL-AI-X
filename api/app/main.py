"""FastAPI application bundling quantum backtester."""

from __future__ import annotations

from fastapi import Depends, FastAPI

from .routers import quantum
from .security import JWTBearer, allowlist_middleware

auth = JWTBearer()

app = FastAPI(title="ANGEL.AI Quantum API", version="0.1.0", dependencies=[Depends(auth)])
app.middleware("http")(allowlist_middleware)
app.include_router(quantum.router, prefix="/api")


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
