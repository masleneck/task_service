from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_async_session
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService
from src.schemas.tasks import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_service(session: AsyncSession = Depends(get_async_session)) -> TaskService:
    return TaskService(TaskRepository(session))

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_service)
):
    return await service.create_task(task_data.model_dump())

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_service)
):
    return await service.get_task(task_id)

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    update_data: dict,
    service: TaskService = Depends(get_service)
):
    return await service.update_task(task_id, update_data)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_service)
):
    await service.delete_task(task_id)