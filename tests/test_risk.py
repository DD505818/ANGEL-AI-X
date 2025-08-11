import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from risk import kelly_fraction, max_drawdown, value_at_risk


def test_kelly_fraction():
    assert round(kelly_fraction(0.6, 1.5), 4) == 0.3333


def test_max_drawdown():
    curve = [100, 120, 90, 150, 80]
    assert round(max_drawdown(curve), 2) == 0.47


def test_value_at_risk():
    returns = [-0.01, 0.02, -0.03, 0.04, -0.05]
    assert value_at_risk(returns, 0.8) == 0.05
