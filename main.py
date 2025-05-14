from fastapi import FastAPI
from api.routers.todo_api import todos_router
from utils.database import create_db_and_tables


app = FastAPI()
app.include_router(todos_router, prefix="/todo")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
