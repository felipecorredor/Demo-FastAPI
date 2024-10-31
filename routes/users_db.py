from fastapi import APIRouter, status, HTTPException
from models.user import User
from database.client import db_client
from database.schemas.user import user_schema, users_schema
from bson import ObjectId
from typing import Union

router = APIRouter(
    prefix="/api/users-db",
    tags=["users-db"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
)

user_client = db_client.users


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[User])
async def get_users():
    try:
        users = user_client.find()
        user_schema_list = users_schema(users)
        return user_schema_list
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: str):
    try:
        user_dict = _search_user("_id", ObjectId(user_id))
        if not user_dict:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user_dict
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    try:
        if _search_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )
        user_dict = user.model_dump(exclude_unset=True)
        user_id = user_client.insert_one(user_dict).inserted_id
        new_user = user_client.find_one({"_id": user_id})
        user_dict_schema = user_schema(new_user)
        return User(**user_dict_schema)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: str, user: User):
    try:
        user_dict = user.model_dump(exclude_unset=True)
        user_replaced = user_client.find_one_and_replace(
            {"_id": ObjectId(user_id)}, user_dict
        )
        if not user_replaced:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        user_updated = _search_user("_id", ObjectId(user_id))
        return user_updated
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    try:
        user_deleted = user_client.find_one_and_delete({"_id": ObjectId(user_id)})
        if not user_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return {"message": "User deleted"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# private methods


def _search_by_email(email: str):
    user = user_client.find_one({"email": email})
    if not user:
        return None
    return User(**user_schema(user))


def _search_user(field: str, key: Union[str, ObjectId]):
    user = user_client.find_one({field: key})
    if not user:
        return None
    return User(**user_schema(user))
