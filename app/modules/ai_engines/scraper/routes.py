from fastapi import APIRouter, HTTPException, Query

from . import service
from .schema import ScrapeHistoryItem, ScrapeRequest, ScrapeResponse

router = APIRouter(prefix="/ai/scraper", tags=["AI Scraper"])


@router.post("/", response_model=ScrapeResponse)
async def scrape(payload: ScrapeRequest):
    try:
        return await service.scrape_service(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {exc}") from exc


@router.get("/history", response_model=list[ScrapeHistoryItem])
async def list_scrape_history(
    user_id: str | None = Query(default=None),
    user_email: str | None = Query(default=None),
    limit: int = Query(default=25, ge=1, le=100),
):
    if not user_id and not user_email:
        raise HTTPException(status_code=400, detail="Provide user_id or user_email")
    return await service.list_user_scrapes_service(user_id=user_id, user_email=user_email, limit=limit)
