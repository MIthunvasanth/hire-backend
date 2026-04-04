from pydantic import BaseModel


class ScrapeRequest(BaseModel):
    url: str
    mode: str = "preview"


class ScrapeResponse(BaseModel):
    url: str
    content: str
    source: str
