"""Basic tests for quantum indicator utilities."""

import numpy as np
from api.app.quantum.indicators import ema, rsi


def test_ema_increasing() -> None:
    series = np.array([1, 2, 3, 4], dtype=float)
    out = ema(series, 2)
    assert out[-1] > out[0]


def test_rsi_bounds() -> None:
    series = np.linspace(1, 10, 10)
    out = rsi(series)
    assert np.all((0 <= out) & (out <= 100))
