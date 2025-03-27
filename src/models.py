from datetime import datetime
from typing import Annotated
from sqlalchemy import Boolean, func
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(
        server_default=func.now(),
        onupdate=datetime.now
    )]
ended_at = Annotated[datetime, mapped_column(
        server_default=func.now(),
        onupdate=datetime.now
    )]

class TaskStatus(enum.Enum):
    for_execution = "for_execution"
    at_work = "at_work"
    review = "review"
    completed = "completed"

class TaskType(enum.Enum):
    task = "task"
    epic = "epic"
    story = "story"
    bug = "bug"

class Task(Base):
    __tablename__ = "tasks"

    name: Mapped[str]
    difficulty: Mapped[int]
    description: Mapped[str]
    status: Mapped[TaskStatus]
    type: Mapped[TaskType]
    if_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    ended_at: Mapped[ended_at]

    author_id: Mapped[int]
    doer_id: Mapped[int]
    parent_id: Mapped[int]
