"""Tests for core risk and position sizing utilities."""

import pytest

from app.core import adaptive_position_size, garch_scaled_atr, kelly_blend


def test_garch_scaled_atr() -> None:
    atr = 2.0
    sigma = 0.5
    scaled = garch_scaled_atr(atr, sigma)
    assert pytest.approx(scaled, rel=1e-6) == atr * (1 + 0.5 * sigma)


def test_adaptive_position_size() -> None:
    size = adaptive_position_size(1000, atr=1.0, sigma=0.2, kelly=0.1, dd_frac=0.0, trend_conf=0.7, regime=True)
    assert size > 0
    size_no_regime = adaptive_position_size(1000, atr=1.0, sigma=0.2, kelly=0.1, dd_frac=0.0, trend_conf=0.7, regime=False)
    assert size_no_regime == 0


def test_kelly_blend_bounds() -> None:
    k = kelly_blend(mu=0.1, sigma=0.2, cvar=0.1)
    assert 0.0 <= k <= 0.25
