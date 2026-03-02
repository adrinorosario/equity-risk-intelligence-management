# TLDR; Equity endpoints (add equities to portfolios, update equity metadata).
# TODO: Implement equity CRUD per SRS FR3 and portfolio linkage.

from fastapi import APIRouter

from app.schemas.equity import EquityCreate, EquityPublic, EquityUpdate
from app.services.portfolio_service import PortfolioService


router = APIRouter()

# NOTE: Intentionally no route implementations yet (structure-only scaffold).
