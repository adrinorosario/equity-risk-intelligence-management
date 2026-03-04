# TLDR; Portfolio/equity management use cases — scaffold only.
# TODO: Implement portfolio CRUD, equity CRUD, and relational integrity checks.

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.equity import Equity
from app.db.models.portfolio import Portfolio
from app.schemas.equity import EquityCreate, EquityPublic, EquityUpdate
from app.schemas.portfolio import PortfolioCreate, PortfolioPublic, PortfolioUpdate


class PortfolioService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_portfolio(self, payload: PortfolioCreate) -> PortfolioPublic:
        portfolio = Portfolio(
            user_id=payload.user_id,
            portfolio_name=payload.portfolio_name,
            description=payload.description,
        )
        self.db.add(portfolio)
        await self.db.commit()
        await self.db.refresh(portfolio)
        return PortfolioPublic.model_validate(portfolio, from_attributes=True)

    async def update_portfolio(self, portfolio_id: int, payload: PortfolioUpdate) -> PortfolioPublic:
        portfolio = await self.db.get(Portfolio, portfolio_id)
        if portfolio is None:
            raise ValueError("Portfolio not found")

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(portfolio, field, value)

        await self.db.commit()
        await self.db.refresh(portfolio)
        return PortfolioPublic.model_validate(portfolio, from_attributes=True)

    async def add_equity(self, payload: EquityCreate) -> EquityPublic:
        portfolio = await self.db.get(Portfolio, payload.portfolio_id)
        if portfolio is None:
            raise ValueError("Portfolio not found")

        equity = Equity(
            portfolio_id=payload.portfolio_id,
            company_name=payload.company_name,
            sector=payload.sector,
            market_value=payload.market_value,
            exchange=payload.exchange,
            purchase_date=payload.purchase_date,
        )
        self.db.add(equity)
        await self.db.commit()
        await self.db.refresh(equity)
        return EquityPublic.model_validate(equity, from_attributes=True)

    async def update_equity(self, equity_id: int, payload: EquityUpdate) -> EquityPublic:
        equity = await self.db.get(Equity, equity_id)
        if equity is None:
            raise ValueError("Equity not found")

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(equity, field, value)

        await self.db.commit()
        await self.db.refresh(equity)
        return EquityPublic.model_validate(equity, from_attributes=True)

    async def list_portfolios_for_user(self, user_id: int) -> list[PortfolioPublic]:
        stmt: Select[tuple[Portfolio]] = select(Portfolio).where(Portfolio.user_id == user_id)
        result = await self.db.execute(stmt)
        portfolios = result.scalars().all()
        return [PortfolioPublic.model_validate(p, from_attributes=True) for p in portfolios]

    async def list_equities_for_portfolio(self, portfolio_id: int) -> list[EquityPublic]:
        stmt: Select[tuple[Equity]] = select(Equity).where(Equity.portfolio_id == portfolio_id)
        result = await self.db.execute(stmt)
        equities = result.scalars().all()
        return [EquityPublic.model_validate(e, from_attributes=True) for e in equities]
