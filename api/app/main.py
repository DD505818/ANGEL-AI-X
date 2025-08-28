"""FastAPI application bundling quantum backtester."""

from __future__ import annotations

from fastapi import FastAPI

from .routers import quantum

app = FastAPI(title="ANGEL.AI Quantum API", version="0.1.0")
app.include_router(quantum.router, prefix="/api")


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
