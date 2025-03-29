from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.kafka.consumer import KafkaConsumer
from src.kafka.producer import producer as kafka_producer
import asyncio
from loguru import logger
from src.api.v1 import v1_routers

class NewApp:
    @classmethod
    def create_app(cls) -> FastAPI:
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # Запускаем Kafka consumer при старте
            consumer = KafkaConsumer()
            consumer_task = asyncio.create_task(consumer.run())
            logger.info("Kafka consumer started")
            
            try:
                # Здесь приложение работает
                yield
            finally:
                # Корректное завершение при остановке
                logger.info("Stopping Kafka consumer...")
                consumer_task.cancel()
                try:
                    await consumer_task
                except asyncio.CancelledError:
                    logger.debug("Consumer task cancelled")
                
                logger.info("Stopping Kafka producer...")
                await kafka_producer.stop()
                logger.info("Application stopped")

        app = FastAPI(
            title="Task Service",
            lifespan=lifespan,
            docs_url="/api/docs",
            redoc_url="/api/redoc",
            version="1.0.0"
        )

        # Подключаем роутеры
        for router in v1_routers:
            app.include_router(router, prefix="/api/v1")

        return app