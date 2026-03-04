# Risk assessment endpoints (compute volatility/exposure/scores at equity & portfolio level).

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import DbSession, get_current_active_user
from app.schemas.risk import RiskAssessmentCreate, RiskAssessmentPublic, RiskMetricPublic
from app.schemas.user import UserPublic
from app.services.risk_service import RiskService


router = APIRouter()


@router.post("/assess", response_model=RiskAssessmentPublic, status_code=status.HTTP_201_CREATED)
async def assess_equity_risk(
    payload: RiskAssessmentCreate,
    db=DbSession,
    current_user: UserPublic = Depends(get_current_active_user),
) -> RiskAssessmentPublic:
    # Ensure analyst_id matches the authenticated user for now.
    enforced_payload = RiskAssessmentCreate(
        equity_id=payload.equity_id,
        metric_id=payload.metric_id,
        analyst_id=current_user.user_id,
        risk_score=payload.risk_score,
        assessment_date=payload.assessment_date,
        remarks=payload.remarks,
    )
    service = RiskService(db)
    try:
        return await service.assess_equity_risk(enforced_payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/assessments", response_model=list[RiskAssessmentPublic])
async def list_assessments(
    portfolio_id: int = Query(..., description="Portfolio ID to list assessments for"),
    db=DbSession,
    current_user: UserPublic = Depends(get_current_active_user),
) -> list[RiskAssessmentPublic]:
    service = RiskService(db)
    return await service.list_assessments_for_portfolio(portfolio_id, current_user.user_id)


@router.get("/metrics", response_model=list[RiskMetricPublic])
async def list_metrics(
    db=DbSession,
    current_user: UserPublic = Depends(get_current_active_user),
) -> list[RiskMetricPublic]:
    service = RiskService(db)
    return await service.list_metrics()
