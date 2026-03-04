# FastAPI application entrypoint (mount routers, middleware, startup/shutdown hooks).

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: initialise DB engine, create tables, and seed default risk metrics."""
    from sqlalchemy.ext.asyncio import async_sessionmaker
    from app.db.postgres import init_engine
    from app.services.risk_service import RiskService

    engine = await init_engine()

    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed default risk metrics
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        await RiskService.ensure_default_metrics(session)

    yield
    await engine.dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging()

    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_v1_router, prefix="/api/v1")
    return app


app = create_app()
