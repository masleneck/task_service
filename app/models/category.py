from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Category(Base):
    # __tablename__ = "categories"
    __abstract__ = True  
    
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        CITEXT(120), 
        unique=True
    )

    # many2many
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="categories",
        secondary="task_categories", # название таблицы, через которую связы задачи и категории (переопределим в dynamic_models)
        viewonly=True, # только для чтения
    )