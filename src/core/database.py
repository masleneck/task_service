from sqlalchemy import Integer, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from loguru import logger
from src.core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(id={self.id})>'


# Фабрика сессий с настройками
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_size=20,        # Размер пула соединений
    max_overflow=10,     # Максимальное количество соединений поверх pool_size
    echo=False           # Логировать SQL 
)
logger.debug(f"Connecting to database: {settings.DATABASE_URL_asyncpg}")


async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Не сбрасывать состояние объектов после commit
    autoflush=False
    )


async def get_async_session():
    """Генератор сессий для Dependency Injection в FastAPI"""
    async with async_session_maker() as session:
        yield session


async def check_db_connection():
    """Проверка подключения к БД"""
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.success("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False