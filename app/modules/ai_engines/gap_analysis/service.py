import json
from datetime import datetime, timezone

from openai import AsyncOpenAI
from openai import OpenAIError

from app.core.config import settings
from app.utils.helpers import normalize_mongo_doc
from app.modules.ai_engines.resume_parser import repository as resume_parser_repository

from . import repository
from .schema import GapActionPlanItem, GapAnalyzeRequest, GapAnalyzeResponse, GapSkillBar


async def create_gap_analysis_service(data: dict) -> str:
    return await repository.create_gap_analysis(data)


async def get_gap_analysis_service(gap_analysis_id: str) -> dict | None:
    return normalize_mongo_doc(await repository.get_gap_analysis(gap_analysis_id))


async def list_gap_analyses_service() -> list[dict]:
    items = await repository.get_all_gap_analyses()
    normalized: list[dict] = []
    for item in items:
        doc = normalize_mongo_doc(item)
        if not doc:
            continue
        normalized.append(_normalize_history_doc(doc))
    return normalized


async def list_user_gap_analyses_service(user_id: str | None, user_email: str | None, limit: int = 30) -> list[dict]:
    items = await repository.get_gap_analyses_for_user(user_id=user_id, user_email=user_email, limit=limit)
    normalized: list[dict] = []
    for item in items:
        doc = normalize_mongo_doc(item)
        if not doc:
            continue
        normalized.append(_normalize_history_doc(doc))
    return normalized


def _normalize_history_doc(doc: dict) -> dict:
    now_iso = datetime.now(timezone.utc).isoformat()

    if not isinstance(doc.get("job"), dict):
        doc["job"] = {
            "id": doc.get("job_id", "unknown-job"),
            "title": "Unknown role",
            "company": "Unknown company",
            "skills": [],
        }
    else:
        doc["job"].setdefault("id", doc.get("job_id", "unknown-job"))
        doc["job"].setdefault("title", "Unknown role")
        doc["job"].setdefault("company", "Unknown company")
        doc["job"].setdefault("skills", [])

    doc.setdefault("created_at", now_iso)
    doc.setdefault("match_score", 0)
    doc.setdefault("matched_skills", [])
    doc.setdefault("missing_skills", [])
    doc.setdefault("weak_skills", [])
    doc.setdefault("skill_bars", [])
    doc.setdefault("insights", "")
    doc.setdefault("role_fit_summary", "")
    doc.setdefault("missing_explanations", [])
    doc.setdefault("strengths", [])
    doc.setdefault("interview_risks", [])
    doc.setdefault("action_plan", [])
    doc.setdefault("user_id", None)
    doc.setdefault("user_email", None)

    return doc


async def update_gap_analysis_service(gap_analysis_id: str, data: dict) -> None:
    await repository.update_gap_analysis(gap_analysis_id, data)


async def delete_gap_analysis_service(gap_analysis_id: str) -> None:
    await repository.delete_gap_analysis(gap_analysis_id)


def _safe_json_loads(content: str) -> dict:
    cleaned = (content or "{}").strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        payload = json.loads(cleaned)
        return payload if isinstance(payload, dict) else {}
    except json.JSONDecodeError as exc:
        raise ValueError("Gap analysis model returned invalid JSON") from exc


def _normalize_skill_list(items: object) -> list[str]:
    if not isinstance(items, list):
        return []

    normalized = []
    seen = set()
    for item in items:
        value = str(item).strip()
        if not value:
            continue
        canonical = value.lower()
        if canonical in seen:
            continue
        seen.add(canonical)
        normalized.append(value)
    return normalized


def _normalize_skill_bars(items: object) -> list[GapSkillBar]:
    if not isinstance(items, list):
        return []

    bars: list[GapSkillBar] = []
    for item in items[:10]:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        try:
            value = int(item.get("value", 0))
        except (TypeError, ValueError):
            value = 0
        value = max(0, min(100, value))
        bars.append(GapSkillBar(name=name, value=value))

    return bars


def _normalize_action_plan(items: object) -> list[GapActionPlanItem]:
    if not isinstance(items, list):
        return []

    normalized: list[GapActionPlanItem] = []
    for item in items[:8]:
        if not isinstance(item, dict):
            continue

        title = str(item.get("title", "")).strip()
        reason = str(item.get("reason", "")).strip()
        if not title or not reason:
            continue

        next_steps = _normalize_skill_list(item.get("next_steps"))
        priority = str(item.get("priority", "")).strip() or None
        normalized.append(
            GapActionPlanItem(
                title=title,
                reason=reason,
                next_steps=next_steps[:4],
                priority=priority,
            )
        )

    return normalized


async def analyze_live_gap_service(payload: GapAnalyzeRequest) -> GapAnalyzeResponse:
    latest_resume = await resume_parser_repository.get_latest_parsed_resume(payload.user_id, payload.user_email)
    if not latest_resume:
        raise ValueError("No parsed resume found. Upload and parse your resume first.")

    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured on backend")

    resume_sections = latest_resume.get("sections", {})
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    prompt_payload = {
        "resume_sections": resume_sections,
        "job": payload.job.model_dump(),
    }

    try:
        completion = await client.chat.completions.create(
            model=settings.openai_gap_model,
            response_format={"type": "json_object"},
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert technical recruiter and career coach. "
                        "Analyze resume-vs-job fit and return ONLY valid JSON with this schema: "
                        "{"
                        '\"match_score\": integer 0-100, '
                        '\"matched_skills\": string[], '
                        '\"missing_skills\": string[], '
                        '\"weak_skills\": string[], '
                        '\"skill_bars\": [{\"name\": string, \"value\": integer 0-100}], '
                        '\"insights\": string, '
                        '\"role_fit_summary\": string, '
                        '\"missing_explanations\": string[], '
                        '\"strengths\": string[], '
                        '\"interview_risks\": string[], '
                        '\"action_plan\": [{\"title\": string, \"reason\": string, \"next_steps\": string[], \"priority\": string}]'
                        "}. "
                        "Rules: focus on concrete skills/tools/experience, keep arrays concise (3-12 items), "
                        "ensure skill_bars has at most 10 entries, and write direct feedback to candidate in second person."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(prompt_payload),
                },
            ],
        )
    except OpenAIError as exc:
        raise ValueError(f"Gap analysis LLM request failed: {exc}") from exc

    parsed = _safe_json_loads(completion.choices[0].message.content or "{}")
    matched = _normalize_skill_list(parsed.get("matched_skills"))
    missing = _normalize_skill_list(parsed.get("missing_skills"))
    weak = _normalize_skill_list(parsed.get("weak_skills"))
    skill_bars = _normalize_skill_bars(parsed.get("skill_bars"))
    strengths = _normalize_skill_list(parsed.get("strengths"))
    missing_explanations = _normalize_skill_list(parsed.get("missing_explanations"))
    interview_risks = _normalize_skill_list(parsed.get("interview_risks"))
    action_plan = _normalize_action_plan(parsed.get("action_plan"))

    try:
        match_score = int(parsed.get("match_score", 0))
    except (TypeError, ValueError):
        match_score = 0
    match_score = max(0, min(100, match_score))

    insights = str(parsed.get("insights", "")).strip()
    if not insights:
        insights = "The analysis completed, but no detailed insight text was returned by the model."

    role_fit_summary = str(parsed.get("role_fit_summary", "")).strip()
    if not role_fit_summary:
        role_fit_summary = (
            "You have some alignment with this role, but there are notable capability gaps to close "
            "before you can compete strongly."
        )

    if not missing_explanations and missing:
        missing_explanations = [
            f"You are currently missing experience or evidence in: {skill}."
            for skill in missing[:8]
        ]

    record = {
        "candidate_id": payload.user_id or payload.user_email or "anonymous",
        "user_id": payload.user_id,
        "user_email": payload.user_email.lower() if payload.user_email else None,
        "job_id": payload.job.id,
        "missing_skills": missing,
        "matched_skills": matched,
        "weak_skills": weak,
        "match_score": match_score,
        "job": payload.job.model_dump(),
        "resume_id": str(latest_resume.get("_id", "")),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "insights": insights,
        "role_fit_summary": role_fit_summary,
        "missing_explanations": missing_explanations,
        "strengths": strengths,
        "interview_risks": interview_risks,
        "action_plan": [item.model_dump() for item in action_plan],
        "skill_bars": [bar.model_dump() for bar in skill_bars],
    }
    saved_id = await repository.create_gap_analysis(record)

    return GapAnalyzeResponse(
        id=saved_id,
        match_score=match_score,
        matched_skills=matched,
        missing_skills=missing,
        weak_skills=weak,
        skill_bars=skill_bars,
        insights=insights,
        role_fit_summary=role_fit_summary,
        missing_explanations=missing_explanations,
        strengths=strengths,
        interview_risks=interview_risks,
        action_plan=action_plan,
        job=payload.job,
    )
