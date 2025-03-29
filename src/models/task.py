from datetime import datetime
from sqlalchemy import Boolean, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from src.core.database import Base

class TaskStatus(enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"
    REVIEW = "REVIEW"

class TaskType(enum.Enum):
    TASK = "TASK"
    EPIC = "EPIC"
    STORY = "STORY"
    BUG = "BUG"

class Task(Base):
    __tablename__ = "tasks"

    name: Mapped[str] = mapped_column(String(255))
    difficulty: Mapped[int] = mapped_column(default=1)
    description: Mapped[str] = mapped_column(String(1000))
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.TODO)
    type: Mapped[TaskType] = mapped_column(default=TaskType.TASK)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())
    ended_at: Mapped[datetime | None]

    author_id: Mapped[str] = mapped_column(String(36))  # UUID
    doer_id: Mapped[str | None] = mapped_column(String(36))
    parent_id: Mapped[str | None] = mapped_column(String(36))


    # many2many
    categories: Mapped[list["Category"]] = relationship(
        back_populates="tasks",
        secondary="task_categories",  # название таблицы, через которую связы задачи и категории
        lazy="selectin", # для m2m
    )

    # many2many
    sprints: Mapped[list["Sprint"]] = relationship(
        back_populates="tasks",
        secondary="sprint_tasks",  # название таблицы, через которую связы задачи и категории
        lazy="selectin",
    )