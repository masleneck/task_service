from datetime import datetime
from loguru import logger
from sqlalchemy import select
from src.core.database import async_session_maker, async_engine, Base
from src.models.task import Task, TaskStatus, TaskType


class AsyncCRUD:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            logger.success('Tables dropped successfully!')
            await conn.run_sync(Base.metadata.create_all)
            logger.success('Tables created successfully!')

    @staticmethod
    async def insert_tasks():
        async with async_session_maker() as session:
            task1  = Task(
                name="Создать репозиторий сервис задач",
                difficulty=3,
                description="Создание и управление задачами – добавление, редактирование, удаление, назначение исполнителей.",
                status=TaskStatus.archived,
                type=TaskType.task,
                if_active=False,
                created_at=datetime(2025, 3, 27, 10, 0, 0), 
                updated_at=datetime(2025, 3, 27, 13, 0, 0),
                ended_at=datetime(2025, 3, 27, 15, 0, 0),
                author_id="uid123456789"
                )
            task2  = Task(
                name="Реализовать сущность задача",
                difficulty=5,
                description="Сущность 'Задача' – это базовая единица системы, которая описывает действие, требующее выполнения.",
                status=TaskStatus.in_progress,
                type=TaskType.epic,
                author_id="uid12sdfghyujk23"
            )
            session.add_all([task1, task2]) 
            await session.commit()
        logger.success('Data tasks inserted successfully!')

    @staticmethod
    async def select_tasks():
        async with async_session_maker() as session:
            query = select(Task)
            result = await session.execute(query)
            tasks = result.scalars().all()
            for task in tasks:
                logger.info(f"Task ID: {task.id}, Taskname: {task.name}")

    @staticmethod
    async def update_task(task_id: int = 2, new_taskname: str = "Реализовать сущность категория"):
        async with async_session_maker() as session:
            task_1 = await session.get(Task, task_id) 
            task_1.name = new_taskname
            await session.commit()
            logger.success(f'Data task ID={task_id} update successfully!')
