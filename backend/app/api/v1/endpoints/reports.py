# TLDR; Reporting endpoints (generate/export risk reports, dashboards summaries).
# TODO: Implement reporting per SRS FR5 and support PDF/CSV exports.

from fastapi import APIRouter

from app.schemas.report import ReportCreate, ReportPublic
from app.services.report_service import ReportService


router = APIRouter()

# NOTE: Intentionally no route implementations yet (structure-only scaffold).
