# TLDR; MongoDB client wiring (Motor).
# TODO: Define collections, indexes, and a small repository layer for document/time-series use cases.

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings


def get_mongo_client() -> AsyncIOMotorClient:
    settings = get_settings()
    return AsyncIOMotorClient(settings.mongo_dsn)


def get_mongo_db() -> AsyncIOMotorDatabase:
    settings = get_settings()
    client = get_mongo_client()
    return client[settings.mongo_db]
