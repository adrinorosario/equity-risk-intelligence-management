# TLDR; Risk metric computation interface (volatility, exposure, concentration, etc).
# TODO: Implement metric calculators and a registry to map DB metrics -> compute functions.

import numpy as np
import pandas as pd

from app.core.exceptions import NotImplementedFeatureError


class RiskMetricsEngine:
    def compute_volatility(self, returns: pd.Series) -> float:
        raise NotImplementedFeatureError("compute_volatility not implemented")

    def compute_exposure(self, positions: pd.DataFrame) -> pd.Series:
        raise NotImplementedFeatureError("compute_exposure not implemented")

    def compute_concentration(self, weights: pd.Series) -> float:
        raise NotImplementedFeatureError("compute_concentration not implemented")
