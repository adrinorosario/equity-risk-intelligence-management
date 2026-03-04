# TLDR; Risk metric computation interface (volatility, exposure, concentration, etc).
# TODO: Implement metric calculators and a registry to map DB metrics -> compute functions.

import numpy as np
import pandas as pd


class RiskMetricsEngine:
    """Core risk metric computations used by the ERIMS engine."""

    trading_days_per_year: int = 252

    def compute_volatility(self, returns: pd.Series) -> float:
        """Compute annualized volatility from a series of returns."""
        clean = returns.dropna()
        if clean.empty:
            return float("nan")
        daily_std = clean.std(ddof=1)
        return float(daily_std * np.sqrt(self.trading_days_per_year))

    def compute_exposure(self, positions: pd.DataFrame) -> pd.Series:
        """Compute normalized exposures from a positions DataFrame.

        Expects a column 'market_value'; falls back to equal weights if missing or total is zero.
        """
        if positions.empty:
            return pd.Series(dtype=float)

        if "market_value" in positions.columns:
            values = positions["market_value"].fillna(0.0).astype(float)
            total = values.sum()
            if total > 0:
                weights = values / total
                return pd.Series(weights.values, index=positions.get("company_name", positions.index))

        # Fallback: equal weights
        n = len(positions)
        if n == 0:
            return pd.Series(dtype=float)
        equal_weight = 1.0 / n
        return pd.Series(
            [equal_weight] * n,
            index=positions.get("company_name", positions.index),
        )

    def compute_concentration(self, weights: pd.Series) -> float:
        """Compute a simple concentration metric using the Herfindahl–Hirschman Index."""
        clean = weights.dropna().astype(float)
        if clean.empty:
            return float("nan")
        hhi = float(np.square(clean).sum())
        return hhi

    def compute_risk_score(self, volatility: float, concentration: float) -> float:
        """Combine volatility and concentration into a 0–100 risk score."""
        if np.isnan(volatility) or np.isnan(concentration):
            return float("nan")

        # Simple normalization heuristics
        vol_norm = min(volatility / 0.5, 1.0)  # assume 50% annual vol as very high
        conc_norm = min(concentration / 0.5, 1.0)  # 0.5 ~ highly concentrated

        score_0_1 = 0.6 * vol_norm + 0.4 * conc_norm
        return float(score_0_1 * 100.0)
