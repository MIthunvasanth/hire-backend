import asyncio
import json
from urllib.parse import parse_qs, urlparse
from datetime import datetime, timezone

import httpx
from openai import AsyncOpenAI
from openai import OpenAIError

from app.core.config import settings
from app.modules.ai_engines.gap_analysis import repository as gap_repository
from app.utils.helpers import normalize_mongo_doc

from . import repository
from .schema import StudyDayPlan, StudyModuleTest, StudyPlanResponse, StudyReferenceItem, StudyReferenceResponse, StudySubModule, StudyTask


def _safe_json_loads(content: str) -> dict:
    cleaned = (content or "{}").strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    payload = json.loads(cleaned)
    return payload if isinstance(payload, dict) else {}


def _extract_youtube_embed_url(raw_url: str | None) -> str | None:
    if not raw_url:
        return None

    parsed = urlparse(raw_url)
    host = parsed.netloc.lower()
    if "youtube.com" in host:
        video_id = parse_qs(parsed.query).get("v", [None])[0]
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        if parsed.path.startswith("/embed/"):
            return raw_url
    if "youtu.be" in host:
        video_id = parsed.path.strip("/")
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
    return None


def _map_reference_item(item: dict) -> StudyReferenceItem | None:
    if not isinstance(item, dict):
        return None

    url = str(item.get("url") or item.get("img_src") or "").strip()
    title = str(item.get("title") or item.get("pretty_url") or "").strip()
    if not url or not title:
        return None

    thumbnail_url = (
        str(item.get("thumbnail_src") or item.get("thumbnail") or item.get("img_src") or "").strip() or None
    )
    source = str(item.get("engine") or item.get("source") or "").strip() or None
    snippet = str(item.get("content") or item.get("description") or "").strip() or None

    return StudyReferenceItem(
        title=title,
        url=url,
        source=source,
        thumbnail_url=thumbnail_url,
        embed_url=_extract_youtube_embed_url(url),
        snippet=snippet,
    )


async def _search_searxng(query: str, categories: str) -> list[StudyReferenceItem]:
    params = {
        "q": query,
        "categories": categories,
        "format": "json",
        "safesearch": 1,
    }
    async with httpx.AsyncClient(timeout=settings.searxng_timeout_seconds) as client:
        response = await client.get(f"{settings.searxng_base_url}/search", params=params)

    if response.status_code >= 400:
        raise ValueError(f"SearXNG search failed: {response.status_code} {response.text}")

    payload = response.json()
    items: list[StudyReferenceItem] = []
    for raw_item in payload.get("results", []):
        mapped = _map_reference_item(raw_item)
        if mapped:
            items.append(mapped)
    return items


async def get_study_references_service(query: str, limit: int = 6) -> StudyReferenceResponse:
    from app.core.database import redis_client

    search_query = query.strip()
    if not search_query:
        raise ValueError("Query is required")

    cache_key = f"searxng:refs:{search_query}:{limit}"
    try:
        cached = await redis_client.get(cache_key)
        if cached:
            return StudyReferenceResponse.model_validate_json(cached)
    except Exception:
        pass  # Redis unavailable — proceed without cache

    try:
        video_results, image_results = await asyncio.gather(
            _search_searxng(search_query, "videos"),
            _search_searxng(search_query, "images"),
        )
    except httpx.TimeoutException as exc:
        raise ValueError("SearXNG timed out while fetching references") from exc
    except httpx.RequestError as exc:
        raise ValueError(f"Unable to reach SearXNG: {exc}") from exc

    result = StudyReferenceResponse(
        query=search_query,
        videos=video_results[:limit],
        images=image_results[:limit],
    )
    try:
        await redis_client.setex(cache_key, 86400, result.model_dump_json())
    except Exception:
        pass  # Redis unavailable — skip caching

    return result


def _normalize_plan(items: object) -> list[StudyDayPlan]:
    if not isinstance(items, list):
        return []

    days: list[StudyDayPlan] = []
    for idx, item in enumerate(items[:14], start=1):
        if not isinstance(item, dict):
            continue
        topic = str(item.get("topic", "")).strip() or f"Day {idx} Focus"
        tasks_raw = item.get("tasks", [])
        tasks: list[StudyTask] = []
        if isinstance(tasks_raw, list):
            for t_idx, task in enumerate(tasks_raw[:8], start=1):
                if not isinstance(task, dict):
                    continue
                title = str(task.get("title", "")).strip()
                if not title:
                    continue
                resource = str(task.get("resource", "")).strip() or None

                submodules: list[StudySubModule] = []
                subs_raw = task.get("submodules", [])
                if isinstance(subs_raw, list):
                    for s_idx, sub in enumerate(subs_raw[:6], start=1):
                        if not isinstance(sub, dict):
                            continue
                        sub_title = str(sub.get("title", "")).strip()
                        if not sub_title:
                            continue
                        submodules.append(
                            StudySubModule(
                                id=f"d{idx}-t{t_idx}-s{s_idx}",
                                title=sub_title,
                                description=str(sub.get("description", "")).strip() or None,
                                completed=False,
                            )
                        )

                tasks.append(
                    StudyTask(
                        id=f"d{idx}-t{t_idx}",
                        title=title,
                        resource=resource,
                        completed=False,
                        submodules=submodules,
                    )
                )

        if not tasks:
            tasks = [StudyTask(id=f"d{idx}-t1", title="Review role requirements and take notes", completed=False)]

        # Parse module_test
        module_test: StudyModuleTest | None = None
        mt_raw = item.get("module_test")
        if isinstance(mt_raw, dict):
            mt_title = str(mt_raw.get("title", "")).strip() or f"Day {idx} Module Test"
            mt_type = str(mt_raw.get("type", "interview")).strip()
            if mt_type not in ("interview", "coding"):
                mt_type = "interview"
            mt_questions = [q for q in mt_raw.get("questions", []) if isinstance(q, str) and q.strip()]
            module_test = StudyModuleTest(
                id=f"d{idx}-test",
                title=mt_title,
                type=mt_type,
                questions=mt_questions[:8],
                description=str(mt_raw.get("description", "")).strip() or None,
                completed=False,
            )

        # Parse overall_test
        overall_test: StudyModuleTest | None = None
        ot_raw = item.get("overall_test")
        if isinstance(ot_raw, dict):
            ot_title = str(ot_raw.get("title", "")).strip() or f"Day {idx} Comprehensive Test"
            ot_type = str(ot_raw.get("type", "coding")).strip()
            if ot_type not in ("interview", "coding"):
                ot_type = "coding"
            ot_questions = [q for q in ot_raw.get("questions", []) if isinstance(q, str) and q.strip()]
            overall_test = StudyModuleTest(
                id=f"d{idx}-overall-test",
                title=ot_title,
                type=ot_type,
                questions=ot_questions[:5],
                description=str(ot_raw.get("description", "")).strip() or None,
                completed=False,
            )

        days.append(StudyDayPlan(
            day=idx,
            topic=topic,
            tasks=tasks,
            module_test=module_test,
            overall_test=overall_test
        ))

    return days


async def generate_study_plan_service(gap_analysis_id: str, user_id: str | None, user_email: str | None) -> StudyPlanResponse:
    gap_item = await gap_repository.get_gap_analysis(gap_analysis_id)
    gap = normalize_mongo_doc(gap_item)
    if not gap:
        raise ValueError("Gap analysis not found for study plan generation")

    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured on backend")

    payload = {
        "job": gap.get("job", {}),
        "match_score": gap.get("match_score", 0),
        "missing_skills": gap.get("missing_skills", []),
        "weak_skills": gap.get("weak_skills", []),
        "insights": gap.get("insights", ""),
        "action_plan": gap.get("action_plan", []),
    }

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    try:
        completion = await client.chat.completions.create(
            model=settings.openai_gap_model,
            response_format={"type": "json_object"},
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a career coach creating detailed study plans with submodules and tests. "
                        "Return ONLY valid JSON matching this exact schema: "
                        '{"title": string, "summary": string, "plan": ['
                        '{"topic": string, "tasks": ['
                        '{"title": string, "resource": string|null, "submodules": [{"title": string, "description": string}]}'
                        '], "module_test": {"title": string, "type": "interview", "questions": [string]}, '
                        '"overall_test": {"title": string, "type": "coding", "questions": [string], "description": string}'
                        "}]}. "
                        "Rules: plan 5-10 days; each day 3-5 tasks; each task 2-4 submodules (concrete actionable sub-steps); "
                        "module_test type 'interview' with 3-5 conceptual questions about the day topic; "
                        "overall_test type 'interview' with 3-5 conceptual questions covering the whole plan; "
                        "all content specific to the provided skill gaps, concise and actionable."
                    ),
                },
                {"role": "user", "content": json.dumps(payload)},
            ],
        )
    except OpenAIError as exc:
        raise ValueError(f"Study plan LLM request failed: {exc}") from exc

    parsed = _safe_json_loads(completion.choices[0].message.content or "{}")
    title = str(parsed.get("title", "")).strip() or "AI Generated Study Plan"
    summary = str(parsed.get("summary", "")).strip() or "A personalized plan to close your role-specific skill gaps."
    plan = _normalize_plan(parsed.get("plan"))

    if not plan:
        plan = [
            StudyDayPlan(
                day=1,
                topic="Core Gap Recovery",
                tasks=[StudyTask(id="d1-t1", title="Create a focused checklist for missing skills", completed=False)],
            )
        ]

    created_at = datetime.now(timezone.utc).isoformat()
    record = {
        "gap_analysis_id": gap_analysis_id,
        "user_id": user_id,
        "user_email": user_email.lower() if user_email else None,
        "title": title,
        "summary": summary,
        "plan": [day.model_dump() for day in plan],
        "created_at": created_at,
    }
    saved_id = await repository.create_study_plan(record)

    return StudyPlanResponse(
        id=saved_id,
        gap_analysis_id=gap_analysis_id,
        user_id=user_id,
        user_email=user_email.lower() if user_email else None,
        title=title,
        summary=summary,
        plan=plan,
        created_at=created_at,
    )


async def list_study_plans_service(user_id: str | None, user_email: str | None, limit: int = 30) -> list[StudyPlanResponse]:
    items = await repository.list_study_plans_for_user(user_id=user_id, user_email=user_email, limit=limit)
    payload: list[StudyPlanResponse] = []
    for item in items:
        normalized = normalize_mongo_doc(item)
        if not normalized:
            continue
        payload.append(StudyPlanResponse(**normalized))
    return payload


async def update_task_completion_service(plan_id: str, task_id: str, completed: bool) -> None:
    item = await repository.get_study_plan(plan_id)
    plan = normalize_mongo_doc(item)
    if not plan:
        raise ValueError("Study plan not found")

    for day_index, day in enumerate(plan.get("plan", [])):
        # Check top-level tasks
        for task_index, task in enumerate(day.get("tasks", [])):
            if task.get("id") == task_id:
                await repository.update_field_completion(
                    plan_id, f"plan.{day_index}.tasks.{task_index}.completed", completed
                )
                return
            # Check submodules
            for sub_index, sub in enumerate(task.get("submodules", [])):
                if sub.get("id") == task_id:
                    await repository.update_field_completion(
                        plan_id,
                        f"plan.{day_index}.tasks.{task_index}.submodules.{sub_index}.completed",
                        completed,
                    )
                    return
        # Check module_test
        module_test = day.get("module_test") or {}
        if module_test.get("id") == task_id:
            await repository.update_field_completion(
                plan_id, f"plan.{day_index}.module_test.completed", completed
            )
            return
        # Check overall_test
        overall_test = day.get("overall_test") or {}
        if overall_test.get("id") == task_id:
            await repository.update_field_completion(
                plan_id, f"plan.{day_index}.overall_test.completed", completed
            )
            return

    raise ValueError("Task not found in study plan")
