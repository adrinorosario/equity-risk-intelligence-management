# TLDR; Portfolio optimizer scaffolds (PyPortfolioOpt + CVXPY).
# TODO: Implement optimizer interface that returns target weights and diagnostics.

import numpy as np
import pandas as pd
from pypfopt import EfficientFrontier, expected_returns, risk_models


class PortfolioOptimizer:
    """Mean–variance optimizer using PyPortfolioOpt."""

    def optimize(
        self,
        price_history: pd.DataFrame,
        *,
        method: str = "max_sharpe",
        weight_bounds: tuple[float, float] = (0.0, 1.0),
    ) -> dict[str, dict]:
        if price_history.empty or price_history.shape[1] < 1:
            raise ValueError("Price history must contain at least one asset")

        mu = expected_returns.mean_historical_return(price_history)
        sigma = risk_models.sample_cov(price_history)

        ef = EfficientFrontier(mu, sigma, weight_bounds=weight_bounds)

        if method == "min_vol":
            raw_weights = ef.min_volatility()
        else:
            raw_weights = ef.max_sharpe()

        cleaned_weights = ef.clean_weights()
        perf = ef.portfolio_performance()
        expected_return, expected_volatility, sharpe = perf

        weights = {symbol: float(weight) for symbol, weight in cleaned_weights.items() if weight > 0}

        return {
            "weights": weights,
            "metrics": {
                "expected_return": float(expected_return),
                "expected_volatility": float(expected_volatility),
                "sharpe": float(sharpe),
            },
        }
