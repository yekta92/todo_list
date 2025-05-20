from fastapi import FastAPI
from api.routers.todo_api import todos_router
from utils.database import create_db_and_tables
from contextlib import asynccontextmanager


# app = FastAPI()




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    create_db_and_tables()
    yield
    # (Optional) Shutdown logic



app = FastAPI(lifespan=lifespan)
app.include_router(todos_router, prefix="/todo")
