import loguru
from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_acyncpg
)
loguru.logger.debug(f"Connecting to database: {settings.DATABASE_URL_acyncpg}")

async_session_maker = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(id={self.id})>'
