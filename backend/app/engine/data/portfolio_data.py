# TLDR; Portfolio data access layer for analytics (positions, weights, exposures) — scaffold only.
# TODO: Load portfolios/equities from Postgres and create analytics-ready frames.

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotImplementedFeatureError


class PortfolioDataSource:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def load_portfolio_positions(self, portfolio_id: int) -> pd.DataFrame:
        raise NotImplementedFeatureError("load_portfolio_positions not implemented")
