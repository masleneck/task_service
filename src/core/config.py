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
    KAFKA_PROJECT_TOPIC: str 
    KAFKA_TASK_TOPIC: str 
    KAFKA_GROUP_ID: str

    @property
    def DATABASE_URL_acyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
        )

settings = Settings()

if __name__ == "__main__":
    logger.info("=== Current Configuration ===")
    logger.info(f"PostgreSQL: {settings.DATABASE_URL_acyncpg}")
    logger.info(f"Kafka Servers: {settings.KAFKA_BOOTSTRAP_SERVERS}")
    logger.info(
        f"Kafka Topics: Projects={settings.KAFKA_PROJECT_TOPIC}, Tasks={settings.KAFKA_TASK_TOPIC}, Group= {settings.KAFKA_GROUP_ID}"
        )