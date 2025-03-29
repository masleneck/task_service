import asyncio
from src.core.database import async_engine, Base, check_db_connection
from loguru import logger
from src.models import(
    Task, TaskStatus, TaskType, Category, TaskCategory, Sprint, SprintTask
    )

async def reset_db():
    """Сброс и инициализация БД"""
    if not await check_db_connection():
        raise RuntimeError("Database connection failed")
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("Tables dropped")
        await conn.run_sync(Base.metadata.create_all)
        logger.success("Tables created")

if __name__ == "__main__":
    asyncio.run(reset_db())
    
    # py -m tests.test_db