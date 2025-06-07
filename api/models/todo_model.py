from typing import Optional, Annotated
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field

from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from utils.database import Base
import enum


class TodoItem(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
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
    class Config:
        orm_mode = True 



class StatusEnum(str, enum.Enum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"

class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
