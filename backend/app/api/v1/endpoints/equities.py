# TLDR; Equity endpoints (add equities to portfolios, update equity metadata).
# TODO: Implement equity CRUD per SRS FR3 and portfolio linkage.

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import DbSession, get_current_active_user
from app.db.models.equity import Equity
from app.db.models.portfolio import Portfolio
from app.schemas.equity import EquityPublic, EquityUpdate
from app.schemas.user import UserPublic
from app.services.portfolio_service import PortfolioService


router = APIRouter()


async def _ensure_equity_belongs_to_user(
    equity_id: int,
    db,
    current_user: UserPublic,
) -> Equity:
    equity = await db.get(Equity, equity_id)
    if equity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equity not found")

    portfolio = await db.get(Portfolio, equity.portfolio_id)
    if portfolio is None or portfolio.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equity not found")

    return equity


@router.put("/{equity_id}", response_model=EquityPublic)
async def update_equity(
    equity_id: int,
    payload: EquityUpdate,
    db=DbSession,
    current_user: UserPublic = Depends(get_current_active_user),
) -> EquityPublic:
    await _ensure_equity_belongs_to_user(equity_id, db, current_user)
    service = PortfolioService(db)
    try:
        return await service.update_equity(equity_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{equity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equity(
    equity_id: int,
    db=DbSession,
    current_user: UserPublic = Depends(get_current_active_user),
) -> None:
    equity = await _ensure_equity_belongs_to_user(equity_id, db, current_user)
    await db.delete(equity)
    await db.commit()
