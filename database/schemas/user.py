def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "role": user["role"]
    }


def users_schema(users) -> list[dict]:
    return [user_schema(user) for user in users]
