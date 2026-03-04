# TLDR; Report generation orchestration — scaffold only.
# TODO: Implement report assembly, storage, and export (PDF/CSV) per SRS FR5.

from datetime import date

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.equity import Equity
from app.db.models.risk import RiskAssessment
from app.schemas.report import ReportCreate, ReportPublic


class ReportService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_report(self, payload: ReportCreate) -> ReportPublic:
        """Create a lightweight report summary based on latest risk assessments."""
        # For now, this is a virtual report that is not persisted in its own table.
        # We aggregate latest risk scores per equity for the given portfolio.
        stmt_equities: Select[tuple[Equity]] = select(Equity).where(Equity.portfolio_id == payload.portfolio_id)
        equities_result = await self.db.execute(stmt_equities)
        equities = equities_result.scalars().all()

        equity_ids = [e.equity_id for e in equities]
        if not equity_ids:
            # Return an empty-but-valid report
            return ReportPublic(
                report_id=0,
                portfolio_id=payload.portfolio_id,
                created_by_user_id=payload.created_by_user_id,
                report_type=payload.report_type,
                created_at=date.today(),
            )

        stmt_assessments = (
            select(
                RiskAssessment.equity_id,
                func.max(RiskAssessment.assessment_date).label("latest_date"),
            )
            .where(RiskAssessment.equity_id.in_(equity_ids))
            .group_by(RiskAssessment.equity_id)
        )
        await self.db.execute(stmt_assessments)

        # Virtual report id of 0 indicates non-persisted summary
        return ReportPublic(
            report_id=0,
            portfolio_id=payload.portfolio_id,
            created_by_user_id=payload.created_by_user_id,
            report_type=payload.report_type,
            created_at=date.today(),
        )
