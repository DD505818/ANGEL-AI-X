"""Lightweight technical indicators for backtests.

All functions operate on numpy arrays and return numpy arrays with
naïve implementations suitable for vectorized backtests.
"""

from __future__ import annotations

import numpy as np


def ema(x: np.ndarray, n: int) -> np.ndarray:
    """Return the exponential moving average of ``x`` with window ``n``."""
    k = 2 / (n + 1)
    out = np.empty_like(x)
    out[:] = np.nan
    s = 0.0
    for i, v in enumerate(x):
        s = v if i == 0 else (k * v + (1 - k) * s)
        out[i] = s
    return out


def rsi(close: np.ndarray, n: int = 14) -> np.ndarray:
    """Compute a simple relative strength index."""
    d = np.diff(close, prepend=close[0])
    up = np.clip(d, 0, None)
    dn = np.clip(-d, 0, None)
    ru = ema(up, n)
    rd = ema(dn, n)
    rs = np.divide(ru, rd, out=np.zeros_like(ru), where=rd > 1e-12)
    return 100 - (100 / (1 + rs))


def macd(close: np.ndarray, fast: int = 12, slow: int = 26, sig: int = 9):
    """Return MACD line, signal and histogram."""
    ema_f = ema(close, fast)
    ema_s = ema(close, slow)
    line = ema_f - ema_s
    signal = ema(line, sig)
    hist = line - signal
    return line, signal, hist


def bollinger(close: np.ndarray, n: int = 20, k: float = 2.0):
    """Return moving average and upper/lower Bollinger Bands."""
    ma = ema(close, n)
    std = np.array([np.std(close[max(0, i - n + 1) : i + 1]) for i in range(len(close))])
    upper = ma + k * std
    lower = ma - k * std
    return ma, upper, lower


def atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, n: int = 14) -> np.ndarray:
    """Average true range over ``n`` periods."""
    prev_close = np.roll(close, 1)
    prev_close[0] = close[0]
    tr = np.maximum(
        high - low,
        np.maximum(np.abs(high - prev_close), np.abs(low - prev_close)),
    )
    return ema(tr, n)


def zscore(x: np.ndarray, n: int = 20) -> np.ndarray:
    """Rolling z-score over window ``n``."""
    res = np.full_like(x, np.nan)
    for i in range(len(x)):
        win = x[max(0, i - n + 1) : i + 1]
        mu = np.mean(win)
        sd = np.std(win) if np.std(win) > 1e-12 else 1.0
        res[i] = (x[i] - mu) / sd
    return res


def realized_vol(ret: np.ndarray, n: int = 20) -> float:
    """Realized volatility over ``n`` returns."""
    return float(np.std(ret[-n:]))


def garch_proxy(ret: np.ndarray, n: int = 200) -> float:
    """A light-weight volatility proxy; replace with real GARCH if desired."""
    return float(np.sqrt(np.var(ret[-n:])))
