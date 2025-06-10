from fastapi import FastAPI
from api.utils.database import create_db_and_tables
from api.routers.todo_api import todos_router
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # (Optional) Shutdown logic



app = FastAPI(lifespan=lifespan)
app.include_router(todos_router, prefix="/todo")
