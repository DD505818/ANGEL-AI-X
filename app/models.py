"""SQLAlchemy ORM models for durable storage."""
from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

Base = declarative_base()


class TimestampMixin:
    """Adds creation timestamp to models."""

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Signal(Base, TimestampMixin):
    __tablename__ = "signals"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(16), nullable=False)
    direction = Column(String(4), nullable=False)
    strength = Column(Float, nullable=False)


class Order(Base, TimestampMixin):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(16), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String(16), nullable=False)


class Fill(Base, TimestampMixin):
    __tablename__ = "fills"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)


class RiskMetric(Base, TimestampMixin):
    __tablename__ = "risk_metrics"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    value = Column(Float, nullable=False)


class Sentiment(Base, TimestampMixin):
    __tablename__ = "sentiment"
    id = Column(Integer, primary_key=True)
    source = Column(String(32), nullable=False)
    score = Column(Float, nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    role = Column(String(32), nullable=False)
    totp_secret = Column(String(32), nullable=True)


engine = create_async_engine(settings.postgres_url, future=True, echo=False)
AsyncSessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def init_db() -> None:
    """Create database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
