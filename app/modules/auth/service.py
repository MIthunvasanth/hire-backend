from app.core.security import create_access_token, hash_password, verify_password

from . import repository


async def register_service(data: dict) -> str:
    existing = await repository.get_user_by_email(data["email"])
    if existing:
        raise ValueError("email already exists")

    user_data = {
        "email": data["email"],
        "password_hash": hash_password(data["password"]),
        "role": "user",
    }
    await repository.create_user(user_data)
    return create_access_token()


async def login_service(data: dict) -> str:
    user = await repository.get_user_by_email(data["email"])
    if not user:
        raise ValueError("invalid credentials")

    if not verify_password(data["password"], user.get("password_hash", "")):
        raise ValueError("invalid credentials")

    return create_access_token()
