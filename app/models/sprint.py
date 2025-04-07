from datetime import date
from sqlalchemy import Boolean, Text, Integer, Date, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Sprint(Base):
    # __tablename__ = "sprints"
    __abstract__ = True  

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

    # many2many
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="sprints",
        secondary="sprint_tasks",  # название таблицы, через которую связы задачи и спринты (переопределим в dynamic_models)
        viewonly=True,
    )