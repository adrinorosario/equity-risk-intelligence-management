# TLDR; Central API v1 router aggregator.
# TODO: Mount endpoint routers and add shared dependencies (auth/roles).

from fastapi import APIRouter

from app.api.v1.endpoints import auth, equities, portfolios, reports, risk, users


api_v1_router = APIRouter()

api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(users.router, prefix="/users", tags=["users"])
api_v1_router.include_router(portfolios.router, prefix="/portfolios", tags=["portfolios"])
api_v1_router.include_router(equities.router, prefix="/equities", tags=["equities"])
api_v1_router.include_router(risk.router, prefix="/risk", tags=["risk"])
api_v1_router.include_router(reports.router, prefix="/reports", tags=["reports"])
