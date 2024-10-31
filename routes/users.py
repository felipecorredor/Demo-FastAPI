from fastapi import APIRouter, status, HTTPException
from models.user import User

router = APIRouter(prefix="/users", tags=["users"])


user_list: list[User] = [
    {"username": "Juan", "email": "juan@example.com", "role": "admin"},
    {"username": "Felipe", "email": "felipe@example.com", "role": "user"},
]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users():
    return user_list


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    user_list.append(user)
    return user


@router.get("/{email}", status_code=status.HTTP_200_OK)
async def get_user_by_email(email: str):
    found = False
    for user in user_list:
        if user["email"] == email:
            found = True
            return user

    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(email: str):
    for user in user_list:
        if user["email"] == email:
            user_list.remove(user)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
