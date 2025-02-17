from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    role: str
