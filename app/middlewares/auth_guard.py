from fastapi import HTTPException, Request


async def auth_guard(request: Request) -> None:
    if "authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Unauthorized")
