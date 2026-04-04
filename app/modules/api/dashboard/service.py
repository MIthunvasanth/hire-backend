from . import repository


async def get_stats_service() -> dict:
    return await repository.counts()
