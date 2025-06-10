# app/routers.py
import datetime
from typing import List
from uuid import UUID
from uuid import uuid4
from fastapi import HTTPException, status, APIRouter, Depends 
from api.models.todo_model import TodoItem
from sqlmodel import Session,select

from ..utils.database import get_session

todos_router = APIRouter()


todos = TodoItem(
    id=UUID(int=0x12345678123456781234567812345678),
    title="Title of the Todo item",
    description="Optional description of the Todo item",
    status="pending",
    created_at=datetime.datetime.now(),
    updated_at = datetime.datetime.now(),

)



@todos_router.post("/todos/create", response_model=TodoItem, status_code=status.HTTP_201_CREATED)
def create_todo(
    todoitem: TodoItem,
    session: Session = Depends(get_session),
):
    # Validation
    if not todoitem.title or not todoitem.title.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title must be provided and non-empty",
        )

    if not isinstance(todoitem.completed, bool):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Completed must be a boolean",
        )

    todoitem.created_at = datetime.datetime.utcnow()
    if not todoitem.id:
        todoitem.id = uuid4()

    session.add(todoitem)
    session.commit()
    session.refresh(todoitem)
    return todoitem




@todos_router.post("/create", response_model=None)
def create_todo(
    todoitem: TodoItem, 
    session: Session = Depends(get_session),
):
    if not todoitem.title or not todoitem.title.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title must be provided and non-empty",
        )

    if not isinstance(todoitem.completed, bool):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Completed must be a boolean",
        )

    todo = TodoItem(
        id=todoitem.id,
        title=todoitem.title,
        description=todoitem.description,
        completed=todoitem.completed,
        created_at=datetime.datetime.utcnow(),
        status=todoitem.status or "active",
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@todos_router.get("/get_todos", response_model=List[TodoItem])
def get_todos(session: Session = Depends(get_session),
) -> List[TodoItem]:
    todos = session.exec(select(TodoItem)).all()
    return todos


@todos_router.get("/get_one_todo/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: str,session: Session = Depends(get_session)
,) -> TodoItem:
    todo = session.get(TodoItem, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="todo not found")
    return todo


@todos_router.get("/update/{todo_id}", response_model=TodoItem)
def update_todo(todo_update: TodoItem,session: Session = Depends(get_session),
) -> TodoItem:
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
        status=todo_update.status,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@todos_router.delete("/delete/{todo_id}")
def delete_todo(id: UUID,session: Session = Depends(get_session),
) -> dict:
    todo = session.get(TodoItem, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()

    return {"message": "Todo item deleted successfully"}
