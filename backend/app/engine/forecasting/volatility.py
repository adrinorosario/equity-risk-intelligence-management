# TLDR; Volatility forecasting scaffolds (e.g., rolling stats, GARCH, ML).
# TODO: Implement volatility estimators and forecasts used by risk scoring.

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from statsmodels.tsa.api import ExponentialSmoothing

from app.core.exceptions import NotImplementedFeatureError


class VolatilityForecaster:
    def forecast(self, returns: pd.Series) -> float:
        raise NotImplementedFeatureError("forecast not implemented")
