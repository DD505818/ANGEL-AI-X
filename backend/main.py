"""FastAPI application entry point."""
from fastapi import FastAPI

from backend.settings import settings
from backend.security.auth import JWTAuth
from backend.security.ip_allowlist import IPAllowlistMiddleware
from backend.routers import governance, health, risk, strategy, tiles, wallet


app = FastAPI(title="ANGEL.AI Gateway", version="13.9-ultra")
app.add_middleware(IPAllowlistMiddleware, allowlist=settings.admin_ips, protected_prefix="/admin")
app.state.auth = JWTAuth(secret=settings.jwt_secret)

# router registrations
app.include_router(health.router)
app.include_router(wallet.router, prefix="/wallet")
app.include_router(strategy.router, prefix="/strategy")
app.include_router(governance.router, prefix="/admin")
app.include_router(risk.router, prefix="/risk")
app.include_router(tiles.router, prefix="/ws")
