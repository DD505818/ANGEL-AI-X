"""Adaptive risk sizing and dynamic thresholds."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .indicators import realized_vol


@dataclass
class SizingParams:
    """Risk sizing parameters."""
    base_risk: float = 0.02
    target_vol: float = 0.015
    dd_scale: float = 2.0
    max_fraction: float = 0.20
    min_fraction: float = 0.01


@dataclass
class DynamicThresholdsConfig:
    """Controls dynamic widening of thresholds in volatile regimes."""
    widen_in_high_vol: bool = True
    widen_factor: float = 1.25


def adaptive_fraction(returns: np.ndarray, dd: float, sp: SizingParams) -> float:
    """Size positions inversely to realized volatility and drawdown."""
    rv = max(1e-6, realized_vol(returns, 20))
    frac = sp.base_risk * (sp.target_vol / rv) * (1 - sp.dd_scale * dd)
    return float(min(sp.max_fraction, max(sp.min_fraction, frac)))


def apply_dynamic_thresholds(tp: float, sl: float, rsi_low: float, rsi_high: float, sigma: float, cfg: DynamicThresholdsConfig):
    """Adjust thresholds when volatility ``sigma`` is high."""
    if cfg.widen_in_high_vol and sigma > 0.02:
        tp, sl = tp * cfg.widen_factor, sl * cfg.widen_factor
        rsi_low, rsi_high = rsi_low - 2, rsi_high + 2
    return tp, sl, rsi_low, rsi_high


@dataclass
class RunConfig:
    """Run parameters for the backtester."""
    reinvest: float = 0.70
    seed: int = 42


@dataclass
class FeesConfig:
    """Transaction cost parameters in basis points."""
    taker_bp: float = 5.0
    maker_bp: float = 5.0
    slippage_bp: float = 5.0
    borrow_bp_daily: float = 0.0
    funding_bp_daily: float = 0.0


@dataclass
class VenueCosts:
    """Venue-specific cost weights."""
    maker_fee: float = 0.0002
    taker_fee: float = 0.0005
    weight_fee: float = 0.35
    weight_slip: float = 0.30
    weight_lat: float = 0.20
    weight_outage: float = 0.15
    depth_threshold: float = 100000.0

    @staticmethod
    def defaults() -> dict[str, "VenueCosts"]:
        """Return default venue cost settings."""
        return {
            "binance": VenueCosts(maker_fee=0.0002, taker_fee=0.0004),
            "bybit": VenueCosts(maker_fee=0.0002, taker_fee=0.0005),
            "coinbase": VenueCosts(maker_fee=0.0004, taker_fee=0.0006),
            "kraken": VenueCosts(maker_fee=0.0002, taker_fee=0.0005),
            "alpaca": VenueCosts(maker_fee=0.0001, taker_fee=0.0005),
        }
