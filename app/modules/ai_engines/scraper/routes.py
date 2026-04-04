from fastapi import APIRouter

from . import service
from .schema import ScrapeRequest

router = APIRouter(prefix="/ai/scraper", tags=["AI Scraper"])


@router.post("/")
async def scrape(payload: ScrapeRequest):
    return await service.scrape_service(payload.model_dump())
