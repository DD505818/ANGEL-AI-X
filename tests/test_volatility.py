from app.models.volatility import realized_volatility, value_at_risk


def test_realized_volatility():
    returns = [0.01, -0.02, 0.015]
    vol = realized_volatility(returns)
    assert vol > 0


def test_value_at_risk():
    returns = [-0.01, 0.02, -0.03, 0.01]
    var = value_at_risk(returns, 0.95)
    assert var >= 0
