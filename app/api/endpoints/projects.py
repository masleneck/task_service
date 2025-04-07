from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_session, async_engine
from app.models import init_project_tables, get_project_models
from app.schemas.projects import ProjectCreateRequest


router = APIRouter(tags=["Projects"])

@router.post("/init_project", summary="Создает таблицы для нового проекта")
async def init_project(
    request: ProjectCreateRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """Создает таблицы для нового проекта"""
    models = await init_project_tables(request.slug, session)
    await session.commit()
    return {
        "status": "success",
        "message": f"Таблицы для проекта '{request.slug}' созданы",
        "tables": list(models.keys())
    }