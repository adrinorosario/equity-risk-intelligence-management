# TLDR; Risk assessment endpoints (compute volatility/exposure/scores at equity & portfolio level).
# TODO: Implement risk calculations per SRS FR4 and call into `engine/risk/` modules.

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import DbSession, get_current_active_user
from app.schemas.risk import RiskAssessmentCreate, RiskAssessmentPublic
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
