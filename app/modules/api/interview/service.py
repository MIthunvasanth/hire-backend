from app.utils.helpers import normalize_mongo_doc

from . import repository
from app.core.database import redis_client

import json


async def create_interview_service(data: dict) -> str:
    return await repository.create_interview(data)


async def get_interview_service(interview_id: str) -> dict | None:
    return normalize_mongo_doc(await repository.get_interview(interview_id))


async def list_interviews_service() -> list[dict]:
    items = await repository.get_all_interviews()
    return [normalize_mongo_doc(i) for i in items]


async def update_interview_service(interview_id: str, data: dict) -> None:
    await repository.update_interview(interview_id, data)


async def delete_interview_service(interview_id: str) -> None:
    await repository.delete_interview(interview_id)


async def agent_next_question_service(interview_id: str, data: dict) -> dict:
    key = f"interview_agent:{interview_id}"
    raw = await redis_client.get(key)
    history: list[dict] = json.loads(raw) if raw else []

    if data.get("last_answer"):
        history.append({"answer": data["last_answer"]})

    turn = len(history) + 1
    role = (data.get("role") or "").strip() or "Software Engineer"
    level = (data.get("level") or "").strip()
    skills: list[str] = data.get("skills") or []

    skill_hint = skills[(turn - 1) % len(skills)] if skills else None
    if skill_hint:
        question = f"Explain a project where you used {skill_hint} in the context of {role}. What trade-offs did you consider?"
    else:
        question = f"Walk me through a challenging problem you solved as a {role}. What was your approach?"

    if level:
        question = f"({level}) {question}"

    history.append({"question": question})
    await redis_client.set(key, json.dumps(history), ex=60 * 60)

    return {"interview_id": interview_id, "question": question, "turn": turn}
