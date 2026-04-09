from app.core.security import create_access_token, hash_password, verify_password

from . import repository


def _serialize_auth_user(user: dict) -> dict:
    return {
        "id": str(user.get("_id", "")),
        "name": user.get("name", ""),
        "email": user.get("email", ""),
        "role": user.get("role", "user"),
    }


async def register_service(data: dict) -> dict:
    if data["password"] != data["confirm_password"]:
        raise ValueError("passwords do not match")

    existing = await repository.get_user_by_email(data["email"])
    if existing:
        raise ValueError("email already exists")

    user_data = {
        "name": data["name"],
        "email": data["email"],
        "password_hash": hash_password(data["password"]),
        "role": "user",
    }
    user_id = await repository.create_user(user_data)
    return {
        "access_token": create_access_token(),
        "user": {
            "id": user_id,
            "name": user_data["name"],
            "email": user_data["email"],
            "role": user_data["role"],
        },
    }


async def login_service(data: dict) -> dict:
    user = await repository.get_user_by_email(data["email"])
    if not user:
        raise ValueError("invalid credentials")

    if not verify_password(data["password"], user.get("password_hash", "")):
        raise ValueError("invalid credentials")

    return {
        "access_token": create_access_token(),
        "user": _serialize_auth_user(user),
    }
