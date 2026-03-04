"""High-level analytics pipelines that orchestrate risk analysis and optimization."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from app.engine.data.market_data import MarketDataSource
from app.engine.data.portfolio_data import align_prices_to_positions, compute_log_returns
from app.engine.forecasting.volatility import VolatilityForecaster, forecast_panel
from app.engine.optimization.optimizer import PortfolioOptimizer
from app.engine.risk.metrics import RiskMetricsEngine


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def run_equity_risk_analysis(
    symbol: str,
    price_history: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """Compute risk metrics and forecast for a single equity."""
    if price_history is None or price_history.empty:
        mds = MarketDataSource()
        price_history = await mds.fetch_price_history(symbol)

    if symbol not in price_history.columns and price_history.shape[1] == 1:
        # Assume single column is the symbol
        price_history = price_history.rename(columns={price_history.columns[0]: symbol})

    returns = compute_log_returns(price_history[[symbol]])
    rm = RiskMetricsEngine()
    current_vol = rm.compute_volatility(returns[symbol])

    forecaster = VolatilityForecaster()
    forecast_vol = forecaster.forecast(returns[symbol])

    # Single-asset exposure and concentration are trivial.
    volatility = current_vol
    concentration = 1.0
    risk_score = rm.compute_risk_score(volatility, concentration)

    return {
        "metadata": {
            "symbol": symbol,
            "generated_at": _now_utc_iso(),
        },
        "metrics": {
            "current_volatility": current_vol,
            "concentration": concentration,
            "risk_score": risk_score,
        },
        "forecast": {
            "forecast_volatility": forecast_vol,
        },
        "details": {
            "returns": returns.to_dict(orient="list"),
        },
    }


async def run_portfolio_risk_analysis(
    portfolio_id: int,
    price_history: pd.DataFrame,
    positions: pd.DataFrame,
) -> dict[str, Any]:
    """Aggregate risk across a portfolio."""
    aligned_prices = align_prices_to_positions(price_history, positions)
    returns = compute_log_returns(aligned_prices)

    rm = RiskMetricsEngine()
    exposures = rm.compute_exposure(positions)
    concentration = rm.compute_concentration(exposures)

    per_equity_metrics: dict[str, dict[str, float]] = {}
    for symbol in aligned_prices.columns:
        symbol_returns = returns[symbol]
        vol = rm.compute_volatility(symbol_returns)
        per_equity_metrics[symbol] = {
            "volatility": vol,
        }

    # Simple portfolio volatility approximation using exposures as weights
    cov = returns.cov()
    weights = exposures.reindex(aligned_prices.columns).fillna(0.0).values
    portfolio_var = float(weights @ cov.to_numpy() @ weights)
    portfolio_vol = float(portfolio_var**0.5) if portfolio_var >= 0 else float("nan")
    risk_score = rm.compute_risk_score(portfolio_vol, concentration)

    return {
        "metadata": {
            "portfolio_id": portfolio_id,
            "generated_at": _now_utc_iso(),
        },
        "metrics": {
            "portfolio_volatility": portfolio_vol,
            "concentration": concentration,
            "risk_score": risk_score,
        },
        "details": {
            "per_equity": per_equity_metrics,
            "exposures": exposures.to_dict(),
        },
    }


async def run_portfolio_optimization(
    portfolio_id: int,
    price_history: pd.DataFrame,
    positions: pd.DataFrame,
) -> dict[str, Any]:
    """Optimize portfolio weights and return diagnostics."""
    aligned_prices = align_prices_to_positions(price_history, positions)

    optimizer = PortfolioOptimizer()
    result = optimizer.optimize(aligned_prices)
    target_weights = result["weights"]

    # Current weights from positions
    rm = RiskMetricsEngine()
    current_weights = rm.compute_exposure(positions).to_dict()

    deltas: dict[str, float] = {}
    for symbol, target in target_weights.items():
        current = float(current_weights.get(symbol, 0.0))
        deltas[symbol] = target - current

    return {
        "metadata": {
            "portfolio_id": portfolio_id,
            "generated_at": _now_utc_iso(),
        },
        "optimization": {
            "current_weights": current_weights,
            "target_weights": target_weights,
            "delta_weights": deltas,
            "metrics": result["metrics"],
        },
    }


def map_portfolio_risk_to_assessments(
    portfolio_result: dict[str, Any],
    portfolio_equity_ids: dict[str, int],
    analyst_id: int,
) -> list[dict[str, Any]]:
    """Flatten portfolio risk result into assessment-like dicts."""
    metrics = portfolio_result.get("metrics", {})
    per_equity = portfolio_result.get("details", {}).get("per_equity", {})

    assessments: list[dict[str, Any]] = []

    for symbol, equity_metrics in per_equity.items():
        equity_id = portfolio_equity_ids.get(symbol)
        if equity_id is None:
            continue
        risk_score = equity_metrics.get("volatility") or 0.0
        assessments.append(
            {
                "equity_id": equity_id,
                "metric_name": "Volatility",
                "risk_score": risk_score,
                "analyst_id": analyst_id,
            }
        )

    if "risk_score" in metrics:
        assessments.append(
            {
                "equity_id": None,
                "metric_name": "Portfolio Risk Score",
                "risk_score": metrics["risk_score"],
                "analyst_id": analyst_id,
            }
        )

    return assessments