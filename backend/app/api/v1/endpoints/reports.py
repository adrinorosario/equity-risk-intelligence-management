# Reporting endpoints (generate/export risk reports, dashboard summaries).

from fastapi import APIRouter, Depends, Query

from app.api.deps import DbSession, get_current_active_user
from app.schemas.report import ReportCreate, ReportPublic
from app.schemas.user import UserPublic
from app.services.report_service import ReportService


router = APIRouter()


@router.post("/", response_model=ReportPublic)
async def create_report(
    payload: ReportCreate,
    db=DbSession,
    current_user: UserPublic = Depends(get_current_active_user),
) -> ReportPublic:
    enforced_payload = ReportCreate(
        portfolio_id=payload.portfolio_id,
        created_by_user_id=current_user.user_id,
        report_type=payload.report_type,
    )
    service = ReportService(db)
    return await service.create_report(enforced_payload)


@router.get("/", response_model=list[ReportPublic])
async def list_reports(
    portfolio_id: int = Query(None, description="Filter reports by portfolio"),
    db=DbSession,
    current_user: UserPublic = Depends(get_current_active_user),
) -> list[ReportPublic]:
    service = ReportService(db)
    return await service.list_reports(portfolio_id, current_user.user_id)
