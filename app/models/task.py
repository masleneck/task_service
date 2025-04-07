from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import (
    Boolean, func, String, BigInteger, Text, DateTime, ForeignKey, Index)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.core.database import Base

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
    # __tablename__ = "tasks"
    __abstract__ = True  # Это шаблон

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        index=True,
    )
    complexity: Mapped[int | None] = None 
    description: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    status: Mapped[TaskStatus] = mapped_column(
        default=TaskStatus.TODO,
        server_default="'TODO'",
    )
    type: Mapped[TaskType] = mapped_column(
        default=TaskType.TASK,
        server_default="'TASK'",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
    ) 
    doer_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), 
    )
    parent_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("tasks.id", ondelete="SET NULL"),
    )


    # many2many
    categories: Mapped[list["Category"]] = relationship(
        back_populates="tasks",
        secondary="task_categories",  # название таблицы, через которую связы задачи и категории (переопределим в dynamic_models)
        lazy="selectin", # для m2m
    )

    # many2many
    sprints: Mapped[list["Sprint"]] = relationship(
        back_populates="tasks",
        secondary="sprint_tasks",  # название таблицы, через которую связы задачи и категории (переопределим в dynamic_models)
        lazy="selectin",
    )