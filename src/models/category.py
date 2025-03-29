from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # many2many
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="categories",
        secondary="task_categories", # название таблицы, через которую связы задачи и категории
        viewonly=True, # только для чтения
    )