"""Middleware enforcing an IP allowlist for administrative endpoints."""
from typing import Iterable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class IPAllowlistMiddleware(BaseHTTPMiddleware):
    """Reject requests to protected paths from IPs not in the allowlist."""

    def __init__(self, app, allowlist: Iterable[str], protected_prefix: str = "/admin") -> None:  # type: ignore[override]
        super().__init__(app)
        self._allow = set(allowlist)
        self._prefix = protected_prefix

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        if request.url.path.startswith(self._prefix):
            client_ip = request.client.host
            if client_ip not in self._allow:
                return JSONResponse({"error": "forbidden"}, status_code=403)
        return await call_next(request)
