# app/routers.py
from typing import List
import datetime
from uuid import UUID, uuid4
from fastapi import HTTPException, status, APIRouter, Depends
from utils.database import get_session, create_db_and_tables, SessionDep
from api.models.todo_model import TodoItem
from sqlmodel import Session, select

todos_router = APIRouter()


@todos_router.on_event("startup")
def on_startup():
    create_db_and_tables()


todos = TodoItem(
    id=UUID(int=0x12345678123456781234567812345678),
    title="Title of the Todo item",
    description="Optional description of the Todo item",
    completed=False,
    created_at=datetime.now(),
)


@todos_router.post("/create", response_model=TodoItem)
def create_todos(todoitem: TodoItem, session: SessionDep) -> TodoItem:
    if not todoitem.title:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title must be provided and non-empty",
        )

    if not isinstance(todoitem.completed, bool):
        raise KeyError("Completed must be a boolean")

    if todoitem.id is None:
        id = uuid4()

    if todoitem.created_at is None:
        created_at = datetime.datetime.now()

    todo = TodoItem(
        id=id,
        title=todoitem.title,
        description=todoitem.description,
        completed=todoitem.completed,
        created_at=created_at,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@todos_router.get("/get_todos", response_model=List[TodoItem])
def get_todos(session: Session = Depends(get_session)) -> List[TodoItem]:
    todos = session.exec(select(TodoItem)).all()
    return todos


@todos_router.get("/get_one_todo/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: UUID, session: SessionDep) -> TodoItem:
    todo = session.get(TodoItem, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="todo not found")
    return todo


@todos_router.get("/update/{todo_id}", response_model=TodoItem)
def update_todo(todo_update: TodoItem, session: SessionDep) -> TodoItem:
    todo = session.get(TodoItem, todo_update.id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    todo = TodoItem(
        id=todo_update.id,
        title=todo_update.title,
        description=todo_update.description,
        completed=todo_update.completed,
        created_at=todo_update.created_at,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@todos_router.delete("/delete/{todo_id}")
def delete_todo(id: UUID, session: SessionDep) -> dict:
    todo = session.get(TodoItem, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(todo)
    session.commit()

    return {"message": "Todo item deleted successfully"}
