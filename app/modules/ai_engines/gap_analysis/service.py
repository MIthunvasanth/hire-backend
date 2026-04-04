from app.utils.helpers import normalize_mongo_doc

from . import repository


async def create_gap_analysis_service(data: dict) -> str:
    return await repository.create_gap_analysis(data)


async def get_gap_analysis_service(gap_analysis_id: str) -> dict | None:
    return normalize_mongo_doc(await repository.get_gap_analysis(gap_analysis_id))


async def list_gap_analyses_service() -> list[dict]:
    items = await repository.get_all_gap_analyses()
    return [normalize_mongo_doc(i) for i in items]


async def update_gap_analysis_service(gap_analysis_id: str, data: dict) -> None:
    await repository.update_gap_analysis(gap_analysis_id, data)


async def delete_gap_analysis_service(gap_analysis_id: str) -> None:
    await repository.delete_gap_analysis(gap_analysis_id)
