from aiokafka import AIOKafkaConsumer
from src.core.config import settings
from src.services.project_service import ProjectService
from loguru import logger

class KafkaConsumer:
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            settings.KAFKA_PROJECT_TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=settings.KAFKA_GROUP_ID,
            auto_offset_reset='earliest'
        )
        self.service = ProjectService()

    async def run(self):
        """Основной цикл обработки сообщений"""
        await self.consumer.start()
        logger.info("Kafka consumer started")
        
        try:
            async for msg in self.consumer:
                try:
                    success = await self.service.process_project_event(
                        msg.value.decode()
                    )
                    if not success:
                        logger.warning("Failed to process message")
                except Exception as e:
                    logger.error(f"Message processing error: {e}")
        finally:
            await self.consumer.stop()
            logger.info("Kafka consumer stopped")