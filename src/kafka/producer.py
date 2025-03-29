import json
from aiokafka import AIOKafkaProducer
from src.core.config import settings
from loguru import logger
from typing import Dict, Any

class KafkaProducer:
    """Асинхронный продюсер для Kafka """
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._producer = None
            cls._instance._is_connected = False
        return cls._instance

    async def _ensure_connection(self):
        """Устанавливает подключение если его нет"""
        if not self._is_connected:
            self._producer = AIOKafkaProducer( 
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS, # <- Подключение к кластеру
                compression_type="gzip"  # Опциональное сжатие
            )
            await self._producer.start()
            self._is_connected = True
            logger.info("Kafka producer connected")

    async def send(self, topic: str, message: dict) -> bool:
        try:
            await self._ensure_connection()
            value = json.dumps(message).encode('utf-8')
            
            # Логирование перед отправкой
            logger.debug(f"Sending to {topic}: {value.decode()}")
            
            await self._producer.send_and_wait(
                topic=topic,
                value=value
            )
            logger.success(f"Message sent to {topic}")
            return True
        except Exception as e:
            logger.error(f"Send failed: {str(e)}")
            return False

    async def stop(self):
        """Корректное отключение продюсера"""
        if self._is_connected and self._producer:
            await self._producer.stop()
            self._is_connected = False
            logger.info("Kafka producer disconnected")

producer = KafkaProducer()