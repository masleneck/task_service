from datetime import datetime
from typing import Annotated, Optional
from sqlalchemy import Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from src.database import Base


created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[Optional[datetime], mapped_column(nullable=True, onupdate=func.now())]
ended_at = Annotated[Optional[datetime], mapped_column(nullable=True)]

class TaskStatus(enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    archived = "archived"

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

    # author_id: Mapped[int]
    # doer_id: Mapped[int]
    # parent_id: Mapped[int]
