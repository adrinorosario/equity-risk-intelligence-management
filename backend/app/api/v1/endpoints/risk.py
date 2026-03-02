# TLDR; Risk assessment endpoints (compute volatility/exposure/scores at equity & portfolio level).
# TODO: Implement risk calculations per SRS FR4 and call into `engine/risk/` modules.

from fastapi import APIRouter

from app.schemas.risk import RiskAssessmentCreate, RiskAssessmentPublic
from app.services.risk_service import RiskService


router = APIRouter()

# NOTE: Intentionally no route implementations yet (structure-only scaffold).
