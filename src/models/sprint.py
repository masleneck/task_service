from datetime import datetime
from sqlalchemy import Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base

class Sprint(Base):
    __tablename__ = "sprints"

    start_date: Mapped[datetime] 
    end_date: Mapped[datetime | None]
    purpose: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True)

    # many2many
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="sprints",
        secondary="sprint_tasks",  # название таблицы, через которую связы задачи и спринты
        viewonly=True,
    )