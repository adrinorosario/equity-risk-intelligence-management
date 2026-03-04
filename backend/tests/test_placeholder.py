from math import isclose

import numpy as np
import pandas as pd

from app.engine.forecasting.volatility import VolatilityForecaster
from app.engine.optimization.optimizer import PortfolioOptimizer
from app.engine.risk.metrics import RiskMetricsEngine


def test_compute_volatility_simple_series() -> None:
    engine = RiskMetricsEngine()
    # 1% daily returns for 10 days
    returns = pd.Series([0.01] * 10)
    vol = engine.compute_volatility(returns)
    assert vol > 0


def test_compute_exposure_normalizes_weights() -> None:
    engine = RiskMetricsEngine()
    positions = pd.DataFrame(
        {
            "company_name": ["A", "B"],
            "market_value": [50.0, 50.0],
        }
    )
    weights = engine.compute_exposure(positions)
    assert isclose(weights.sum(), 1.0, rel_tol=1e-6)


def test_concentration_between_zero_and_one() -> None:
    engine = RiskMetricsEngine()
    weights = pd.Series([0.5, 0.5])
    hhi = engine.compute_concentration(weights)
    assert 0 <= hhi <= 1


def test_volatility_forecaster_requires_minimum_window() -> None:
    returns = pd.Series(np.random.normal(0, 0.01, size=10))
    forecaster = VolatilityForecaster(window=30)
    forecast = forecaster.forecast(returns)
    assert np.isnan(forecast)


def test_portfolio_optimizer_returns_weights_and_metrics() -> None:
    np.random.seed(0)
    dates = pd.date_range(start="2020-01-01", periods=60, freq="D")
    prices = pd.DataFrame(
        {
            "A": np.linspace(100, 120, 60),
            "B": np.linspace(50, 55, 60),
        },
        index=dates,
    )
    optimizer = PortfolioOptimizer()
    result = optimizer.optimize(prices)
    weights = result["weights"]
    assert set(weights.keys()) <= {"A", "B"}
    assert 0.99 <= sum(weights.values()) <= 1.01
    metrics = result["metrics"]
    assert "expected_return" in metrics and "expected_volatility" in metrics and "sharpe" in metrics
