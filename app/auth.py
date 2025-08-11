"""JWT authentication with optional TOTP and RBAC."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Annotated, Optional

import pyotp
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .db import get_session
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class Token(BaseModel):
    """JWT access token."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data embedded in JWT tokens."""

    username: str
    role: str


async def get_user(session: AsyncSession, username: str) -> Optional[User]:
    """Retrieve a user from the database."""
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password for storage."""
    return pwd_context.hash(password)


async def authenticate_user(session: AsyncSession, username: str, password: str, totp_code: Optional[str]) -> User:
    """Authenticate user with password and optional TOTP."""
    user = await get_user(session, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if user.totp_secret:
        if not totp_code:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="TOTP required")
        totp = pyotp.TOTP(user.totp_secret)
        if not totp.verify(totp_code):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid TOTP code")
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[AsyncSession, Depends(get_session)]) -> User:
    """Decode JWT and return current user."""
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    user = await get_user(session, username)
    if user is None:
        raise credentials_exception
    return user


def require_role(required_role: str):
    """Dependency factory enforcing RBAC."""

    async def role_checker(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")
        return user

    return role_checker


async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[AsyncSession, Depends(get_session)]) -> Token:
    """OAuth2 password flow endpoint."""
    user = await authenticate_user(session, form_data.username, form_data.password, form_data.scopes[0] if form_data.scopes else None)
    token = create_access_token({"sub": user.username, "role": user.role})
    return Token(access_token=token)
