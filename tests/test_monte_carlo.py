import numpy as np

from app.models.monte_carlo import kelly_fraction, monte_carlo_var


def test_monte_carlo_var():
    rng = np.random.default_rng(0)
    returns = rng.normal(0.001, 0.01, 100)
    var = monte_carlo_var(returns, horizon=5, iterations=1000, alpha=0.95, rng=rng)
    assert var > 0


def test_kelly_fraction():
    frac = kelly_fraction(0.01, 0.04)
    assert 0 < frac < 1
