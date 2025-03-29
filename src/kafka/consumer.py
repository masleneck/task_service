from aiokafka import AIOKafkaConsumer
from loguru import logger
from src.core.config import settings
from src.kafka.workers import ProjectWorker, TaskWorker
import json

class KafkaConsumer:
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            settings.KAFKA_PROJECT_TOPIC,
            settings.KAFKA_TASK_TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=settings.KAFKA_GROUP_ID,
            auto_offset_reset="earliest"
        )
        self.workers = {
            settings.KAFKA_PROJECT_TOPIC: ProjectWorker(),
            settings.KAFKA_TASK_TOPIC: TaskWorker()
        }

    async def run(self):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                worker = self.workers.get(msg.topic)
                if worker:
                    try:
                        message = json.loads(msg.value.decode())
                        await worker.handle(message)
                    except Exception as e:
                        logger.error(f"Message processing failed: {e}")
        finally:
            await self.consumer.stop()