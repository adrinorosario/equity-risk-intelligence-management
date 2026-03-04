# TLDR; Portfolio data access layer for analytics (positions, weights, exposures) — scaffold only.
# TODO: Load portfolios/equities from Postgres and create analytics-ready frames.

import pandas as pd
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.equity import Equity


class PortfolioDataSource:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def load_portfolio_positions(self, portfolio_id: int) -> pd.DataFrame:
        """Load basic position data (symbol proxy and market value) for a portfolio.

        This returns a DataFrame with columns:
        - equity_id
        - company_name
        - market_value
        """
        stmt: Select[tuple[Equity]] = select(Equity).where(Equity.portfolio_id == portfolio_id)
        result = await self.db.execute(stmt)
        equities = result.scalars().all()

        if not equities:
            return pd.DataFrame(columns=["equity_id", "company_name", "market_value"])

        data = [
            {
                "equity_id": e.equity_id,
                "company_name": e.company_name,
                "market_value": float(e.market_value) if e.market_value is not None else 0.0,
            }
            for e in equities
        ]
        return pd.DataFrame(data)


def compute_log_returns(price_history: pd.DataFrame) -> pd.DataFrame:
    """Compute log returns from a price history DataFrame."""
    if price_history.empty:
        return price_history.copy()
    returns = (price_history / price_history.shift(1)).applymap(lambda x: float("nan") if x <= 0 else x)
    returns = returns.apply(lambda col: pd.Series(pd.Series(col).pipe(lambda s: pd.Series(pd.np.log(s))), index=col.index))
    return returns.dropna(how="all")


def align_prices_to_positions(price_history: pd.DataFrame, positions: pd.DataFrame) -> pd.DataFrame:
    """Subset and align price history columns to the symbols present in positions."""
    if price_history.empty or positions.empty:
        return price_history.iloc[0:0].copy()

    symbols = positions["company_name"].unique().tolist()
    existing = [sym for sym in symbols if sym in price_history.columns]
    return price_history[existing].copy()
