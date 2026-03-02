# TLDR; Portfolio endpoints (create/update/manage portfolios).
# TODO: Implement portfolio CRUD per SRS FR2 and enforce user ownership.

from fastapi import APIRouter

from app.schemas.portfolio import PortfolioCreate, PortfolioPublic, PortfolioUpdate
from app.services.portfolio_service import PortfolioService


router = APIRouter()

# NOTE: Intentionally no route implementations yet (structure-only scaffold).
