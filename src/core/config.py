from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger

class Settings(BaseSettings):
    # PostgreSQL
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str 
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_PROJECT_TOPIC: str = "project_events"
    KAFKA_TASK_TOPIC: str = "task_events"
    KAFKA_GROUP_ID: str = "task_service_group"
    KAFKA_AUTO_OFFSET_RESET: str = "earliest"

    @property
    def DATABASE_URL_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
        )

settings = Settings()

if __name__ == "__main__":
    logger.info("=== Current Configuration ===")
    logger.info(f"PostgreSQL: {settings.DATABASE_URL_asyncpg}")
    logger.info(f"Kafka Servers: {settings.KAFKA_BOOTSTRAP_SERVERS}")
    logger.info(f"Project Topic: {settings.KAFKA_PROJECT_TOPIC}")
    logger.info(f"Task Topic: {settings.KAFKA_TASK_TOPIC}")
    logger.info(f"Consumer Group: {settings.KAFKA_GROUP_ID}")