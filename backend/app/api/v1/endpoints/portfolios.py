# TLDR; Portfolio endpoints (create/update/manage portfolios).
# TODO: Implement portfolio CRUD per SRS FR2 and enforce user ownership.

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import DbSession, get_current_active_user
from app.db.models.portfolio import Portfolio
from app.schemas.equity import EquityCreate, EquityPublic
from app.schemas.portfolio import PortfolioCreate, PortfolioPublic, PortfolioUpdate
from app.schemas.user import UserPublic
from app.services.portfolio_service import PortfolioService


router = APIRouter()


@router.post("/", response_model=PortfolioPublic, status_code=status.HTTP_201_CREATED)
async def create_portfolio(
    payload: PortfolioCreate,
    db=DbSession,
    current_user: UserPublic = Depends(get_current_active_user),
) -> PortfolioPublic:
    # Always enforce ownership from the authenticated user, ignoring any user_id in the payload.
    enforced_payload = PortfolioCreate(
        user_id=current_user.user_id,
        portfolio_name=payload.portfolio_name,
        description=payload.description,
    )
    service = PortfolioService(db)
    return await service.create_portfolio(enforced_payload)


@router.get("/", response_model=list[PortfolioPublic])
async def list_portfolios(
    db=DbSession,
    current_user: UserPublic = Depends(get_current_active_user),
) -> list[PortfolioPublic]:
    service = PortfolioService(db)
    return await service.list_portfolios_for_user(current_user.user_id)


@router.get("/{portfolio_id}", response_model=PortfolioPublic)
async def get_portfolio(
    portfolio_id: int,
    db=DbSession,
    current_user: UserPublic = Depends(get_current_active_user),
) -> PortfolioPublic:
    portfolio = await db.get(Portfolio, portfolio_id)
    if portfolio is None or portfolio.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    return PortfolioPublic.model_validate(portfolio, from_attributes=True)


@router.put("/{portfolio_id}", response_model=PortfolioPublic)
async def update_portfolio(
    portfolio_id: int,
    payload: PortfolioUpdate,
    db=DbSession,
    current_user: UserPublic = Depends(get_current_active_user),
) -> PortfolioPublic:
    portfolio = await db.get(Portfolio, portfolio_id)
    if portfolio is None or portfolio.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    service = PortfolioService(db)
    try:
        return await service.update_portfolio(portfolio_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_portfolio(
    portfolio_id: int,
    db=DbSession,
    current_user: UserPublic = Depends(get_current_active_user),
) -> None:
    portfolio = await db.get(Portfolio, portfolio_id)
    if portfolio is None or portfolio.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    await db.delete(portfolio)
    await db.commit()


@router.post("/{portfolio_id}/equities", response_model=EquityPublic, status_code=status.HTTP_201_CREATED)
async def add_equity_to_portfolio(
    portfolio_id: int,
    payload: EquityCreate,
    db=DbSession,
    current_user: UserPublic = Depends(get_current_active_user),
) -> EquityPublic:
    portfolio = await db.get(Portfolio, portfolio_id)
    if portfolio is None or portfolio.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    enforced_payload = EquityCreate(
        portfolio_id=portfolio_id,
        company_name=payload.company_name,
        sector=payload.sector,
        market_value=payload.market_value,
        exchange=payload.exchange,
        purchase_date=payload.purchase_date,
    )
    service = PortfolioService(db)
    try:
        return await service.add_equity(enforced_payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{portfolio_id}/equities", response_model=list[EquityPublic])
async def list_equities_for_portfolio(
    portfolio_id: int,
    db=DbSession,
    current_user: UserPublic = Depends(get_current_active_user),
) -> list[EquityPublic]:
    portfolio = await db.get(Portfolio, portfolio_id)
    if portfolio is None or portfolio.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    service = PortfolioService(db)
    return await service.list_equities_for_portfolio(portfolio_id)
