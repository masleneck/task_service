from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base

class SprintTask(Base):
    __tablename__ = "sprint_tasks"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True,
    )
    sprint_id: Mapped[int] = mapped_column(
        ForeignKey("sprints.id", ondelete="CASCADE"),
        primary_key=True,
    )

