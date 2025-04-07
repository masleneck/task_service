from sqlalchemy import ForeignKey, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class SprintTask(Base):
    # __tablename__ = "sprint_tasks"
    __abstract__ = True  

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
    )
    task_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True,
    )
    sprint_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sprints.id", ondelete="CASCADE"),
        primary_key=True,
    )

