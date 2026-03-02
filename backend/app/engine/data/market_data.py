# TLDR; Market data ingestion + caching layer (prices, returns, metadata) — scaffold only.
# TODO: Implement data pulls (e.g., yfinance), normalization, and persistence (Mongo recommended).

import pandas as pd
import yfinance as yf

from app.core.exceptions import NotImplementedFeatureError


class MarketDataSource:
    async def fetch_price_history(self, symbol: str, *, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        raise NotImplementedFeatureError("fetch_price_history not implemented")
