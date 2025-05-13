from fastapi import FastAPI

from api.routers.todo_api import todos_router


app = FastAPI()

app.include_router(todos_router, prefix="/todo")
