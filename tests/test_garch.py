from app.models.garch import garch_forecast


def test_garch_forecast():
    returns = [0.01, -0.02, 0.015, -0.005]
    var = garch_forecast(returns, omega=0.000001, alpha=0.05, beta=0.9)
    assert var > 0
