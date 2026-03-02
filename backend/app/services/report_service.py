# TLDR; Report generation orchestration — scaffold only.
# TODO: Implement report assembly, storage, and export (PDF/CSV) per SRS FR5.

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotImplementedFeatureError
from app.schemas.report import ReportCreate, ReportPublic


class ReportService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_report(self, payload: ReportCreate) -> ReportPublic:
        raise NotImplementedFeatureError("create_report not implemented")
