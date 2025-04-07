import enum
import uuid
from datetime import date, datetime
from sqlalchemy.dialects.postgresql import UUID, CITEXT
from sqlalchemy import (
    BigInteger, Boolean, Date, DateTime, ForeignKey, Integer, String, Text, func, text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from . import *

def create_project_models(project_slug: str):
    """Создает модели для проекта"""

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

    class BaseTask(Base):
        __tablename__ = f"{project_slug}_tasks"
        
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
            server_default=text("'TODO'"),
        )
        type: Mapped[TaskType] = mapped_column(
            default=TaskType.TASK,
            server_default=text("'TASK'"),
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
            ForeignKey(f"{project_slug}_tasks.id", ondelete="SET NULL"),
        )
        
        categories: Mapped[list["BaseCategory"]] = relationship(
            secondary=f"{project_slug}_task_categories",
            back_populates="tasks",
            lazy="selectin",
        )
        sprints: Mapped[list["BaseSprint"]] = relationship(
            secondary=f"{project_slug}_sprint_tasks",
            back_populates="tasks",
            lazy="selectin",
        )

    class BaseCategory(Base):
        __tablename__ = f"{project_slug}_categories"
        
        id: Mapped[int] = mapped_column(
            Integer, 
            primary_key=True,
        )
        name: Mapped[str] = mapped_column(
            CITEXT(120), 
            unique=True
        )
        
        tasks: Mapped[list["BaseTask"]] = relationship(
            secondary=f"{project_slug}_task_categories",
            back_populates="categories",
            viewonly=True,
        )

    class BaseSprint(Base):
        __tablename__ = f"{project_slug}_sprints"
        
        id: Mapped[int] = mapped_column(
            Integer, 
            primary_key=True,
        )
        start_date: Mapped[date] = mapped_column(
            Date,
        )
        ended_at: Mapped[date] = mapped_column(
            Date,
        )
        purpose: Mapped[str | None] = mapped_column(
            Text,
            default="",
            server_default="",
        )
        is_active: Mapped[bool] = mapped_column(
            Boolean,
            default=True,
            server_default="true",
        )
        
        tasks: Mapped[list["BaseTask"]] = relationship(
            secondary=f"{project_slug}_sprint_tasks",
            back_populates="sprints",
            viewonly=True,
        )

    class BaseTaskCategory(Base):
        __tablename__ = f"{project_slug}_task_categories"
        
        task_id: Mapped[int] = mapped_column(
            BigInteger,
            ForeignKey(f"{project_slug}_tasks.id", ondelete="CASCADE"),
            primary_key=True,
        )
        category_id: Mapped[int] = mapped_column(
            Integer,
            ForeignKey(f"{project_slug}_categories.id", ondelete="CASCADE"),
            primary_key=True,
        )

    class BaseSprintTask(Base):
        __tablename__ = f"{project_slug}_sprint_tasks"
        
        task_id: Mapped[int] = mapped_column(
            BigInteger,
            ForeignKey(f"{project_slug}_tasks.id", ondelete="CASCADE"),
            primary_key=True,
        )
        sprint_id: Mapped[int] = mapped_column(
            Integer,
            ForeignKey(f"{project_slug}_sprints.id", ondelete="CASCADE"),
            primary_key=True,
        )

    return {
        "Task": BaseTask,
        "Category": BaseCategory,
        "Sprint": BaseSprint,
        "TaskCategory": BaseTaskCategory,
        "SprintTask": BaseSprintTask,
    }