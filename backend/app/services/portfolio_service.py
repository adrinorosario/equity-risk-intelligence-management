# TLDR; Portfolio/equity management use cases — scaffold only.
# TODO: Implement portfolio CRUD, equity CRUD, and relational integrity checks.

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotImplementedFeatureError
from app.schemas.equity import EquityCreate, EquityPublic, EquityUpdate
from app.schemas.portfolio import PortfolioCreate, PortfolioPublic, PortfolioUpdate


class PortfolioService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_portfolio(self, payload: PortfolioCreate) -> PortfolioPublic:
        raise NotImplementedFeatureError("create_portfolio not implemented")

    async def update_portfolio(self, portfolio_id: int, payload: PortfolioUpdate) -> PortfolioPublic:
        raise NotImplementedFeatureError("update_portfolio not implemented")

    async def add_equity(self, payload: EquityCreate) -> EquityPublic:
        raise NotImplementedFeatureError("add_equity not implemented")

    async def update_equity(self, equity_id: int, payload: EquityUpdate) -> EquityPublic:
        raise NotImplementedFeatureError("update_equity not implemented")
