from fastapi import HTTPException, Request


def role_guard(required_role: str):
    async def _guard(request: Request) -> None:
        role = request.headers.get("x-role")
        if role != required_role:
            raise HTTPException(status_code=403, detail="Forbidden")

    return _guard
