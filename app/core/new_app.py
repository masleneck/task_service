from fastapi import FastAPI
from app.core.database import check_db_connection
from app.api.routers import main_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not await check_db_connection():
        raise Exception("Failed to connect to the database")
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        title="Task Servise API",
        description='API для тру JiraBass',
        lifespan=lifespan,
        )
    
    # Подключаем роутер
    app.include_router(main_router)
    
    @app.get("/")
    async def root():
        return {"message": "Task Servise API is running"}
    
    return app