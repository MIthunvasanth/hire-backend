import json
import re
import asyncio
from datetime import datetime, timezone

from openai import AsyncOpenAI
from openai import OpenAIError
from playwright.sync_api import sync_playwright

from app.core.config import settings
from app.utils.helpers import normalize_mongo_doc

from . import repository
from .schema import ScrapeHistoryItem, ScrapeResponse


def _clean_text(value: str) -> str:
    condensed = re.sub(r"\s+", " ", value or "").strip()
    return condensed


def _safe_json_loads(content: str) -> dict:
    cleaned = (content or "{}").strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
    payload = json.loads(cleaned)
    return payload if isinstance(payload, dict) else {}


def _scrape_text_with_playwright_sync(url: str) -> tuple[str, str | None]:
        with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                page = browser.new_page()
                try:
                        page.goto(url, wait_until="networkidle", timeout=45000)
                        title = page.title()
                        content = page.evaluate(
                                """
                                () => {
                                    const selectors = [
                                        'main',
                                        'article',
                                        '[role="main"]',
                                        '.job-description',
                                        '.description',
                                        '.job-details',
                                        '.content'
                                    ];
                                    let text = '';
                                    for (const selector of selectors) {
                                        const el = document.querySelector(selector);
                                        if (el && el.innerText && el.innerText.length > text.length) {
                                            text = el.innerText;
                                        }
                                    }
                                    if (!text) {
                                        text = document.body ? document.body.innerText : '';
                                    }
                                    return text || '';
                                }
                                """
                        )
                        return _clean_text(content), title or None
                finally:
                        page.close()
                        browser.close()


async def _scrape_text_with_playwright(url: str) -> tuple[str, str | None]:
        return await asyncio.to_thread(_scrape_text_with_playwright_sync, url)


async def _extract_with_llm(url: str, title: str | None, text: str, mode: str) -> dict:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured on backend")

    prompt_payload = {
        "url": url,
        "page_title": title,
        "mode": mode,
        "content": text[:18000],
    }

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    try:
        completion = await client.chat.completions.create(
            model=settings.openai_gap_model,
            temperature=0.1,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You extract structured data from scraped web content. "
                        "Return only valid JSON. For job pages include fields: "
                        "title, company, location, employment_type, salary, required_skills(string[]), "
                        "responsibilities(string[]), qualifications(string[]), benefits(string[]), "
                        "application_deadline, apply_url, summary."
                    ),
                },
                {"role": "user", "content": json.dumps(prompt_payload)},
            ],
        )
    except OpenAIError as exc:
        raise ValueError(f"Scraper LLM request failed: {exc}") from exc

    return _safe_json_loads(completion.choices[0].message.content or "{}")


async def scrape_service(data: dict) -> ScrapeResponse:
    url = data["url"]
    mode = data.get("mode") or "job"
    user_id = data.get("user_id")
    user_email = data.get("user_email")

    cached = await repository.get_cached(url)
    if cached:
        try:
            payload = json.loads(cached)
            result = ScrapeResponse(
                url=url,
                source="cache",
                title=payload.get("title"),
                raw_text_excerpt=payload.get("raw_text_excerpt", ""),
                extracted=payload.get("extracted", {}),
                user_id=user_id,
                user_email=user_email.lower() if user_email else None,
            )
            return await _persist_scrape_result(result)
        except Exception:
            pass

    scraped_text, title = await _scrape_text_with_playwright(url)
    if not scraped_text:
        raise ValueError("Could not extract readable text from the target URL")

    extracted = await _extract_with_llm(url=url, title=title, text=scraped_text, mode=mode)
    result = ScrapeResponse(
        url=url,
        source="live",
        title=title,
        raw_text_excerpt=scraped_text[:2000],
        extracted=extracted,
        user_id=user_id,
        user_email=user_email.lower() if user_email else None,
    )

    await repository.set_cached(url, json.dumps(result.model_dump()))
    return await _persist_scrape_result(result)


async def _persist_scrape_result(result: ScrapeResponse) -> ScrapeResponse:
    created_at = datetime.now(timezone.utc).isoformat()
    record = {
        "url": result.url,
        "source": result.source,
        "title": result.title,
        "raw_text_excerpt": result.raw_text_excerpt,
        "extracted": result.extracted,
        "created_at": created_at,
        "user_id": result.user_id,
        "user_email": result.user_email.lower() if result.user_email else None,
    }
    saved_id = await repository.create_scrape_record(record)
    result.id = saved_id
    result.created_at = created_at
    return result


async def list_user_scrapes_service(user_id: str | None, user_email: str | None, limit: int = 25) -> list[ScrapeHistoryItem]:
    items = await repository.list_user_scrape_records(user_id=user_id, user_email=user_email, limit=limit)
    payload: list[ScrapeHistoryItem] = []
    for item in items:
        normalized = normalize_mongo_doc(item)
        if not normalized:
            continue
        payload.append(ScrapeHistoryItem(**normalized))
    return payload
