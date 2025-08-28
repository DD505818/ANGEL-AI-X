"""Trading strategies combining price and sentiment signals."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .indicators import rsi, macd, zscore, bollinger, atr


@dataclass
class QBX3Config:
    """Configuration for QuantumBoost X3."""
    rsi_buy_low: float = 30.0
    rsi_sell_high: float = 70.0
    sentiment_buy: float = 0.70
    tp_pct: float = 0.020
    sl_pct: float = 0.010


@dataclass
class SSv2Config:
    """Configuration for SentimentSurge v2."""
    sentiment_buy: float = 0.75
    tp_pct: float = 0.020
    sl_pct: float = 0.010


@dataclass
class ATRTrendArbConfig:
    """Configuration for ATR trend arbitrage."""
    bb_n: int = 20
    bb_k: float = 2.0
    atr_delta: float = 0.10
    tp_pct: float = 0.020
    sl_pct: float = 0.010


@dataclass
class MomentumStacker7Config:
    """Configuration for MomentumStacker7."""
    mom_thresh: float = 0.010
    rsi_low: float = 40.0
    rsi_high: float = 60.0
    tp_pct: float = 0.020
    sl_pct: float = 0.010


def quantumboost_x3(close: np.ndarray, volume: np.ndarray, sentiment: np.ndarray, cfg: QBX3Config):
    """Signal logic for QuantumBoost X3."""
    r = rsi(close)
    m_line, m_sig, _ = macd(close)
    v_ma = np.convolve(volume, np.ones(20) / 20, mode="same")
    entries = (
        (r < cfg.rsi_buy_low)
        & (m_line > m_sig)
        & (volume > v_ma)
        & (sentiment > cfg.sentiment_buy)
    )
    exits = (r > cfg.rsi_sell_high) | (m_line < m_sig)
    return entries, exits, cfg.tp_pct, cfg.sl_pct


def sentimentsurge_v2(close: np.ndarray, volume: np.ndarray, sentiment: np.ndarray, cfg: SSv2Config):
    """Signal logic for SentimentSurge v2."""
    m_line, m_sig, _ = macd(close)
    v_z = zscore(volume, 20)
    sent_gate = np.maximum(0.75, cfg.sentiment_buy + 0.05)
    entries = (m_line > m_sig) & (sentiment > sent_gate) & (v_z > 1.5)
    exits = (sentiment < 0.5) | (m_line < m_sig)
    return entries, exits, cfg.tp_pct, cfg.sl_pct


def atr_trend_arb(close: np.ndarray, high: np.ndarray, low: np.ndarray, cfg: ATRTrendArbConfig):
    """Signal logic for ATR-based trend arbitrage."""
    _, up, lo = bollinger(close, cfg.bb_n, cfg.bb_k)
    a = atr(high, low, close)
    a_delta = np.concatenate([[0], np.diff(a)]) / np.maximum(1e-9, a)
    entries = (close > up) & (a_delta > cfg.atr_delta)
    exits = close < lo
    return entries, exits, cfg.tp_pct, cfg.sl_pct


def momentum_stacker_7(close: np.ndarray, cfg: MomentumStacker7Config):
    """Signal logic for MomentumStacker7."""
    mom = close / np.roll(close, 7) - 1.0
    r = rsi(close)
    entries = (mom > cfg.mom_thresh) & (r >= cfg.rsi_low) & (r <= cfg.rsi_high)
    exits = (mom < 0.0) | (r > 70.0)
    return entries, exits, cfg.tp_pct, cfg.sl_pct
