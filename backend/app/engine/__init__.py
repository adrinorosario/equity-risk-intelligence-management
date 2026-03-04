"""Analytics engine package for ERIMS.

The engine is responsible for:
- Fetching and preparing market data.
- Computing risk metrics (volatility, exposure, concentration, risk scores).
- Forecasting future risk (e.g., volatility).
- Optimizing portfolio allocations.

Public entrypoints for backend services live in ``app.engine.pipelines``.
All functions are pure analytics and operate on pandas DataFrames and simple dicts.
"""

from typing import TypeAlias

import pandas as pd

PriceHistory: TypeAlias = pd.DataFrame
Returns: TypeAlias = pd.DataFrame