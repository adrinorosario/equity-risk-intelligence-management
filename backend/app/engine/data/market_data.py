# TLDR; Market data ingestion + caching layer (prices, returns, metadata) — scaffold only.
# TODO: Implement data pulls (e.g., yfinance), normalization, and persistence (Mongo recommended).

from typing import Final

import pandas as pd
import yfinance as yf


class MarketDataSource:
    """Simple wrapper around yfinance for fetching historical price data."""

    _PRICE_COLUMN: Final[str] = "Adj Close"

    async def fetch_price_history(
        self,
        symbol: str,
        *,
        period: str = "1y",
        interval: str = "1d",
    ) -> pd.DataFrame:
        """Fetch adjusted close prices for a single symbol.

        Returns a DataFrame indexed by datetime with a single column named after the symbol.
        Raises ValueError if data cannot be fetched or is empty.
        """
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)

        if hist.empty or self._PRICE_COLUMN not in hist.columns:
            raise ValueError(f"No price history available for symbol '{symbol}'")

        prices = hist[[self._PRICE_COLUMN]].rename(columns={self._PRICE_COLUMN: symbol})

        if not isinstance(prices.index, pd.DatetimeIndex) or prices.index.empty:
            raise ValueError(f"Invalid price index for symbol '{symbol}'")

        return prices
