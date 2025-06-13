# app/routers.py
import datetime
from typing import List
import uuid 
from uuid import uuid4
from fastapi import HTTPException, status, APIRouter, Depends 
from api.models.todo_model import TodoItem
from sqlmodel import Session,select

from ..utils.database import get_session

todos_router = APIRouter()



@todos_router.post("/create", response_model=TodoItem)
def create_todo(
    todoitem: TodoItem, 
    session: Session = Depends(get_session),
) -> TodoItem:
    
    try:
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
            id=str(uuid4()),
            title=todoitem.title,
            description=todoitem.description,
            completed=todoitem.completed,
            created_at=datetime.datetime.utcnow(),
            status=todoitem.status or "pending",
        )

        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    except Exception as e:
        session.rollback()  # Rollback in case of error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the todo item: {str(e)}"
        )



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
def delete_todo(id: str,session: Session = Depends(get_session),
) -> dict:
    todo = session.get(TodoItem, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()

    return {"message": "Todo item deleted successfully"}
