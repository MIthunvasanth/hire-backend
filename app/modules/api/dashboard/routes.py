from fastapi import APIRouter

from . import service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
async def stats():
    return await service.get_stats_service()
