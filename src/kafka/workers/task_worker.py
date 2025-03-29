from loguru import logger
from src.services.task_service import TaskService
from src.core.database import async_session_maker

class TaskWorker:
    async def handle(self, message: dict) -> bool:
        try:
            async with async_session_maker() as session:
                task_service = TaskService(session)
                # Здесь обработка событий задач
                return True
        except Exception as e:
            logger.error(f"TaskWorker error: {e}")
            return False