# TLDR; Reporting endpoints (generate/export risk reports, dashboards summaries).
# TODO: Implement reporting per SRS FR5 and support PDF/CSV exports.

from fastapi import APIRouter, Depends

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
