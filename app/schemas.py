"""Pydantic models for request validation."""
from __future__ import annotations

from pydantic import BaseModel, Field


class SignalIn(BaseModel):
    symbol: str
    direction: str
    strength: float


class OrderIn(BaseModel):
    symbol: str
    price: float
    capital: float
    win_prob: float = Field(..., ge=0, le=1)
    win_loss_ratio: float = Field(..., gt=0)
    var_limit: float = Field(..., gt=0)


class FillIn(BaseModel):
    order_id: int
    quantity: float
    price: float


class RiskMetricIn(BaseModel):
    name: str
    value: float


class SentimentIn(BaseModel):
    source: str
    score: float
