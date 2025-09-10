"""JWT issuance and verification utilities."""
from datetime import datetime, timedelta, timezone
from typing import Dict

import jwt
from fastapi import HTTPException, status


ALG = "HS256"


class JWTAuth:
    """Helper for issuing and verifying JWT tokens."""

    def __init__(self, secret: str, issuer: str = "angel.ai", audience: str = "angel-clients", ttl: int = 30) -> None:
        self._secret = secret
        self._issuer = issuer
        self._audience = audience
        self._ttl = ttl

    def issue(self, subject: str, role: str) -> str:
        """Create a signed JWT for ``subject`` with the given ``role``."""
        now = datetime.now(timezone.utc)
        payload = {
            "iss": self._issuer,
            "aud": self._audience,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self._ttl)).timestamp()),
            "sub": subject,
            "role": role,
        }
        return jwt.encode(payload, self._secret, algorithm=ALG)

    def verify(self, token: str) -> Dict[str, str]:
        """Validate ``token`` and return its decoded payload."""
        try:
            return jwt.decode(
                token,
                self._secret,
                algorithms=[ALG],
                audience=self._audience,
                issuer=self._issuer,
            )
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_token") from exc
