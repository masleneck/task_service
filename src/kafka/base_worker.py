from abc import ABC, abstractmethod
from loguru import logger

class BaseWorker(ABC):
    @abstractmethod
    async def handle(self, message: dict) -> bool:
        """Обработка сообщения"""
        pass

    async def on_error(self, error: Exception):
        logger.error(f"Worker error: {error}")