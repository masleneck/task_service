from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str   

    @property
    def DATABASE_URL_acyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

if __name__ == '__main__':
    logger.info(f"DB_HOST: {settings.DB_HOST}")
    logger.info(f"DB_PORT: {settings.DB_PORT}")
    logger.info(f"DB_USER: {settings.DB_USER}")
    logger.info(f"DB_PASS: {settings.DB_PASS}")
    logger.info(f"DB_NAME: {settings.DB_NAME}")
    logger.info(f"DATABASE_URL: {settings.DATABASE_URL_acyncpg}")