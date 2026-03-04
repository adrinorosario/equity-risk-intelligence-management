# TLDR; Health check endpoint for uptime monitoring (UptimeRobot, etc).
# Ping this route every 14 minutes to keep Render's free tier from sleeping.

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
