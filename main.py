from fastapi import FastAPI
from typing import Union
from routes.users import router as users_router

app = FastAPI()

app.include_router(users_router)


# main route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# params route
@app.get("/items/{item_id}")
def read_item(
    item_id: int,
    query: Union[str, None] = None,
):
    return {"item_id": item_id, "query": query}
