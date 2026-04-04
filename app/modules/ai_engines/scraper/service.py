from . import repository


async def scrape_service(data: dict) -> dict:
    url = data["url"]
    mode = data.get("mode") or "preview"

    cached = await repository.get_cached(url)
    if cached:
        return {"url": url, "content": cached, "source": "cache"}

    # Placeholder scraper logic (no external HTTP calls here).
    content = f"SCRAPER_PLACEHOLDER[{mode}]: {url}"
    await repository.set_cached(url, content)

    return {"url": url, "content": content, "source": "generated"}
