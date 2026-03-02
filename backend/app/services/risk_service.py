# TLDR; Risk assessment orchestration — scaffold only.
# TODO: Implement risk metric computation (volatility/exposure/scores) via `engine/risk/`.

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotImplementedFeatureError
from app.engine.risk.metrics import RiskMetricsEngine
from app.schemas.risk import RiskAssessmentCreate, RiskAssessmentPublic


class RiskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.engine = RiskMetricsEngine()

    async def assess_equity_risk(self, payload: RiskAssessmentCreate) -> RiskAssessmentPublic:
        raise NotImplementedFeatureError("assess_equity_risk not implemented")
