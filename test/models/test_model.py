from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class TodoItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., description="Title of the Todo item")
    description: Optional[str] = Field(
        None, description="Optional description of the Todo item"
    )
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
