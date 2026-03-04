# Report generation orchestration.

from datetime import date

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.equity import Equity
from app.db.models.portfolio import Portfolio
from app.db.models.risk import RiskAssessment
from app.schemas.report import ReportCreate, ReportPublic


class ReportService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_report(self, payload: ReportCreate) -> ReportPublic:
        """Create a lightweight report summary based on latest risk assessments."""
        stmt_equities: Select[tuple[Equity]] = select(Equity).where(Equity.portfolio_id == payload.portfolio_id)
        equities_result = await self.db.execute(stmt_equities)
        equities = equities_result.scalars().all()

        equity_ids = [e.equity_id for e in equities]
        total_value = sum(float(e.market_value or 0) for e in equities)

        summary = {
            "equity_count": len(equities),
            "total_value": total_value,
            "sectors": list(set(e.sector for e in equities if e.sector)),
        }

        if equity_ids:
            stmt_assessments = (
                select(
                    RiskAssessment.equity_id,
                    func.avg(RiskAssessment.risk_score).label("avg_score"),
                )
                .where(RiskAssessment.equity_id.in_(equity_ids))
                .group_by(RiskAssessment.equity_id)
            )
            result = await self.db.execute(stmt_assessments)
            rows = result.all()
            if rows:
                avg_risk = sum(float(r.avg_score) for r in rows) / len(rows)
                summary["avg_risk_score"] = round(avg_risk, 2)
                summary["assessed_equities"] = len(rows)

        # Virtual report (non-persisted for now)
        return ReportPublic(
            report_id=0,
            portfolio_id=payload.portfolio_id,
            created_by_user_id=payload.created_by_user_id,
            report_type=payload.report_type,
            created_at=date.today(),
            summary=summary,
        )

    async def list_reports(self, portfolio_id: int | None, user_id: int) -> list[ReportPublic]:
        """List reports — since reports are virtual, return empty for now.
        In production, this would query a reports table."""
        return []
