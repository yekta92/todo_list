from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class TodoItem(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(..., description="Title of the Todo item")
    description: Optional[str] = Field(
        None, description="Optional description of the Todo item"
    )
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
