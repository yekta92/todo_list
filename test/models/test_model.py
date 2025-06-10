from typing import Optional, Annotated
from datetime import datetime
from uuid import uuid4
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict



class TodoItem(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: str = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(..., description="Title of the Todo item")
    description: Optional[str] = Field(
        None, description="Optional description of the Todo item"
    )
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    status: Annotated[str, Field(default="pending")] = Field(
        default="pending",
        description="Status of the Todo item, can be 'pending', 'in_progress', or 'completed'",
    )
    model_config = ConfigDict(from_attributes=True)
 

