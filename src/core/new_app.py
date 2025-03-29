from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.kafka.consumer import KafkaConsumer
from src.kafka.producer import producer as kafka_producer
import asyncio
from loguru import logger

class NewApp:
    @classmethod
    def create_app(cls) -> FastAPI:
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # Запуск consumer
            consumer = KafkaConsumer()
            consumer_task = asyncio.create_task(consumer.run())
            
            try:
                logger.info("Application started")
                yield
            finally:
                # Корректное завершение
                logger.info("Shutting down...")
                consumer_task.cancel()
                try:
                    await consumer_task
                except asyncio.CancelledError:
                    pass
                await kafka_producer.stop()
                logger.info("Application stopped")

        return FastAPI(
            title="Task Service",
            lifespan=lifespan,
            docs_url="/api/docs",
            redoc_url="/api/redoc"
        )