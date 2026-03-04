# TLDR; Volatility forecasting scaffolds (e.g., rolling stats, GARCH, ML).
# TODO: Implement volatility estimators and forecasts used by risk scoring.

import numpy as np
import pandas as pd


class VolatilityForecaster:
    """Lightweight volatility forecaster using a rolling window."""

    def __init__(self, window: int = 30, trading_days_per_year: int = 252) -> None:
        self.window = window
        self.trading_days_per_year = trading_days_per_year

    def forecast(self, returns: pd.Series) -> float:
        """Forecast future volatility as the annualized rolling std over the recent window."""
        clean = returns.dropna()
        if len(clean) < self.window:
            return float("nan")

        recent = clean.iloc[-self.window :]
        daily_std = recent.std(ddof=1)
        return float(daily_std * np.sqrt(self.trading_days_per_year))


def forecast_panel(price_history: pd.DataFrame, window: int = 30) -> pd.Series:
    """Forecast volatility for each column in a price history DataFrame."""
    if price_history.empty:
        return pd.Series(dtype=float)

    from app.engine.data.portfolio_data import compute_log_returns

    returns = compute_log_returns(price_history)
    forecaster = VolatilityForecaster(window=window)

    forecasts: dict[str, float] = {}
    for col in returns.columns:
        forecasts[col] = forecaster.forecast(returns[col])

    return pd.Series(forecasts)
