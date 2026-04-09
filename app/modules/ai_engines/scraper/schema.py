from pydantic import BaseModel


class ScrapeRequest(BaseModel):
    url: str
    mode: str = "job"
    user_id: str | None = None
    user_email: str | None = None


class ScrapeResponse(BaseModel):
    id: str | None = None
    url: str
    source: str
    title: str | None = None
    raw_text_excerpt: str
    extracted: dict
    created_at: str | None = None
    user_id: str | None = None
    user_email: str | None = None


class ScrapeHistoryItem(ScrapeResponse):
    id: str
    created_at: str
