import numpy as np

from app.models.technical_indicators import ema, sma


def test_sma():
    data = [1, 2, 3, 4, 5]
    result = sma(data, 3)
    assert np.allclose(result, [2.0, 3.0, 4.0])


def test_ema():
    data = [1, 2, 3, 4, 5]
    result = ema(data, 3)
    assert np.isclose(result[-1], 4.0, atol=1e-1)
