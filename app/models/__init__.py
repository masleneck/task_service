from .task import Task, TaskStatus, TaskType
from .category import Category
from .task_category import TaskCategory
from .sprint import Sprint
from .sprint_task import SprintTask
from .dynamic_models import create_project_models
from typing import Dict, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect, text
from fastapi import HTTPException
from app.core.database import async_engine  

_model_cache: Dict[str, Dict[str, Type]] = {}

async def init_project_tables(project_slug: str, session: AsyncSession) -> Dict[str, Type]:
    """Создает таблицы для проекта"""
    if project_slug in _model_cache:
        return _model_cache[project_slug]
    
    models = create_project_models(project_slug)
    _model_cache[project_slug] = models
    
    # Создаем таблицы через async_engine
    async with async_engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: [model.metadata.create_all(bind=sync_conn) for model in models.values()])
    
    return models

def get_project_models(project_slug: str) -> Dict[str, Type] | None:
    return _model_cache.get(project_slug)

__all__ = [
    'Task', 'TaskStatus', 'TaskType',
    'Category', 'TaskCategory',
    'Sprint', 'SprintTask',
    'init_project_tables',
    'get_project_models'
]