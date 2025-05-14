# app/routers.py
from typing import Optional, List
import datetime
from uuid import UUID, uuid4
from fastapi import HTTPException, status, APIRouter

from api.models.todo_model import TodoItem



todos_router = APIRouter()

todos = [
    TodoItem(
        id=UUID(int=0x12345678123456781234567812345678),
        title="Buy milk",
        description="Get whole milk",
        completed=False,
        created_at=datetime.datetime.now()
    )
]


@todos_router.post("/create", response_model=TodoItem)
def create_todos(
    id: Optional[UUID] = None,
    title: str = None,
    description: Optional[str] = None,
    completed: bool = False,
    created_at = None,
) -> TodoItem:
    if not title:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title must be provided and non-empty",
        )

    if not isinstance(completed, bool):
        raise KeyError("Completed must be a boolean")

    if id is None:
        id = uuid4()

    if created_at is None:
        created_at = datetime.datetime.now()

    todo = TodoItem(
        id=id,
        title=title,
        description=description,
        completed=completed,
        created_at=created_at,
    )

    return todo


@todos_router.get("/get_todos", response_model=List[TodoItem])
def get_todos() -> List[TodoItem]:
    return todos


@todos_router.get("/get_one_todo/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: UUID) -> TodoItem:

    todo = [todo for todo in todos if todo.id == todo_id]
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo[0]


@todos_router.put("/update/{todo_id}", response_model=TodoItem)
def update_todo(
    todo_update: TodoItem = ...,
) -> TodoItem:

    todo = [todo for todo in todos if todo.id == todo_update.id]
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    todo = TodoItem(
        id= todo_update.id,
        title=todo_update.title,
        description=todo_update.description,
        completed=todo_update.completed,
        created_at=todo_update.created_at,
    )

    return todo



@todos_router.delete("/delete/{todo_id}")
def delete_todo(id: UUID) -> dict:

    todo = [todo for todo  in todos if todo.id == id][0]
    del todo

    return  {"message": "Todo item deleted successfully"}
