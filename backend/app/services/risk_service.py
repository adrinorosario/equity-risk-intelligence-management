# Risk assessment orchestration with list capabilities.

from datetime import date

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.equity import Equity
from app.db.models.portfolio import Portfolio
from app.db.models.risk import RiskAssessment, RiskMetric
from app.schemas.risk import RiskAssessmentCreate, RiskAssessmentPublic, RiskMetricPublic


class RiskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def assess_equity_risk(self, payload: RiskAssessmentCreate) -> RiskAssessmentPublic:
        equity = await self.db.get(Equity, payload.equity_id)
        if equity is None:
            raise ValueError("Equity not found")

        # Simple risk score based on market value and sector heuristic
        risk_score = self._compute_simple_risk_score(equity)

        assessment = RiskAssessment(
            equity_id=payload.equity_id,
            metric_id=payload.metric_id,
            analyst_id=payload.analyst_id,
            risk_score=risk_score,
            assessment_date=payload.assessment_date or date.today(),
            remarks=payload.remarks or f"Auto-assessed on {date.today()}",
        )
        self.db.add(assessment)
        await self.db.commit()
        await self.db.refresh(assessment)

        return RiskAssessmentPublic.model_validate(assessment, from_attributes=True)

    def _compute_simple_risk_score(self, equity: Equity) -> float:
        """Compute a simple heuristic risk score (0-100) based on equity attributes."""
        import hashlib

        # Sector-based baseline risk
        sector_risks = {
            "Technology": 55, "Finance": 50, "Healthcare": 45,
            "Energy": 60, "Consumer": 40, "Industrial": 48,
            "Utilities": 30, "Materials": 52, "Real Estate": 42,
        }
        sector = equity.sector or "Unknown"
        base = sector_risks.get(sector, 50)

        # Market value factor: higher value = slightly lower relative risk
        mv = float(equity.market_value or 10000)
        if mv > 500000:
            mv_adj = -8
        elif mv > 100000:
            mv_adj = -3
        elif mv < 10000:
            mv_adj = 10
        else:
            mv_adj = 0

        # Add some deterministic variation based on company name
        name_hash = int(hashlib.md5(equity.company_name.encode()).hexdigest()[:8], 16) % 20 - 10
        score = max(0, min(100, base + mv_adj + name_hash))
        return round(score, 2)

    async def list_assessments_for_portfolio(
        self, portfolio_id: int, user_id: int
    ) -> list[RiskAssessmentPublic]:
        """List all risk assessments for equities belonging to a user's portfolio."""
        # First verify ownership
        portfolio = await self.db.get(Portfolio, portfolio_id)
        if portfolio is None or portfolio.user_id != user_id:
            return []

        # Get equity IDs for this portfolio
        eq_stmt: Select[tuple[Equity]] = select(Equity).where(Equity.portfolio_id == portfolio_id)
        eq_result = await self.db.execute(eq_stmt)
        equity_ids = [e.equity_id for e in eq_result.scalars().all()]

        if not equity_ids:
            return []

        stmt = select(RiskAssessment).where(
            RiskAssessment.equity_id.in_(equity_ids)
        ).order_by(RiskAssessment.assessment_date.desc())
        result = await self.db.execute(stmt)
        assessments = result.scalars().all()

        return [RiskAssessmentPublic.model_validate(a, from_attributes=True) for a in assessments]

    async def list_metrics(self) -> list[RiskMetricPublic]:
        """List all risk metrics."""
        stmt = select(RiskMetric).order_by(RiskMetric.metric_id)
        result = await self.db.execute(stmt)
        metrics = result.scalars().all()
        return [RiskMetricPublic.model_validate(m, from_attributes=True) for m in metrics]

    @staticmethod
    async def ensure_default_metrics(db: AsyncSession) -> None:
        """Seed default risk metrics if the table is empty."""
        stmt = select(RiskMetric)
        result = await db.execute(stmt)
        if result.scalars().first() is not None:
            return  # already seeded

        defaults = [
            RiskMetric(metric_name="Volatility", description="Annualized standard deviation of returns", threshold_value=30.0, category="Market Risk"),
            RiskMetric(metric_name="Exposure", description="Portfolio weight concentration", threshold_value=25.0, category="Concentration"),
            RiskMetric(metric_name="Concentration", description="Herfindahl-Hirschman index of portfolio", threshold_value=50.0, category="Concentration"),
        ]
        for m in defaults:
            db.add(m)
        await db.commit()
