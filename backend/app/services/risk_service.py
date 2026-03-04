# TLDR; Risk assessment orchestration — scaffold only.
# TODO: Implement risk metric computation (volatility/exposure/scores) via `engine/risk/`.

from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.equity import Equity
from app.db.models.risk import RiskAssessment, RiskMetric
from app.engine.data.market_data import MarketDataSource
from app.engine.pipelines import run_equity_risk_analysis, run_portfolio_risk_analysis
from app.schemas.risk import RiskAssessmentCreate, RiskAssessmentPublic


class RiskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def assess_equity_risk(self, payload: RiskAssessmentCreate) -> RiskAssessmentPublic:
        equity = await self.db.get(Equity, payload.equity_id)
        if equity is None:
            raise ValueError("Equity not found")

        # For now, we treat company_name as the symbol for fetching data.
        mds = MarketDataSource()
        price_history = await mds.fetch_price_history(equity.company_name)
        result = await run_equity_risk_analysis(equity.company_name, price_history)

        risk_score = float(result["metrics"]["risk_score"])

        assessment = RiskAssessment(
            equity_id=payload.equity_id,
            metric_id=payload.metric_id,
            analyst_id=payload.analyst_id,
            risk_score=risk_score,
            assessment_date=payload.assessment_date or date.today(),
            remarks=payload.remarks,
        )
        self.db.add(assessment)
        await self.db.commit()
        await self.db.refresh(assessment)

        return RiskAssessmentPublic.model_validate(assessment, from_attributes=True)
