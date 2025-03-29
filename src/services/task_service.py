from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.task_repository import TaskRepository
from src.schemas.tasks import TaskResponse
from src.models.task import Task

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def get_task(self, task_id: int) -> TaskResponse:
        task = await self.repository.get_task(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return TaskResponse.model_validate(task)

    async def create_task(self, task_data: dict) -> TaskResponse:
        try:
            task = await self.repository.create_task(task_data)
            return TaskResponse.model_validate(task)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    async def update_task(self, task_id: int, update_data: dict) -> TaskResponse:
        task = await self.repository.update_task(task_id, update_data)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return TaskResponse.model_validate(task)

    async def delete_task(self, task_id: int) -> None:
        if not await self.repository.delete_task(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )