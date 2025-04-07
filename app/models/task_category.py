from sqlalchemy import ForeignKey, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class TaskCategory(Base):
    # __tablename__ = "task_categories"
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
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True,
    )

