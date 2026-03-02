# TLDR; Portfolio optimizer scaffolds (PyPortfolioOpt + CVXPY).
# TODO: Implement optimizer interface that returns target weights and diagnostics.

import numpy as np
import pandas as pd
import cvxpy as cp
from pypfopt import EfficientFrontier, risk_models, expected_returns

from app.core.exceptions import NotImplementedFeatureError


class PortfolioOptimizer:
    def optimize(self, price_history: pd.DataFrame) -> dict[str, float]:
        raise NotImplementedFeatureError("optimize not implemented")
