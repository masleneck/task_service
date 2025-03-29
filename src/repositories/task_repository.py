from typing import Optional, List
from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from loguru import logger
from src.models import Task, TaskCategory, SprintTask

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_task(self, task_id: int) -> Optional[Task]:
        result = await self.session.execute(
            select(Task)
            .where(Task.id == task_id)
            .options(
                selectinload(Task.categories),
                selectinload(Task.sprints)
            )
        )
        return result.scalar_one_or_none()

    async def create_task(self, task_data: dict) -> Task:
        # Extract relations
        category_ids = task_data.pop('category_ids', [])
        sprint_ids = task_data.pop('sprint_ids', [])
        
        task = Task(**task_data)
        self.session.add(task)
        await self.session.flush()  # Get task ID
        
        # Add many-to-many relations
        for category_id in category_ids:
            self.session.add(TaskCategory(task_id=task.id, category_id=category_id))
        
        for sprint_id in sprint_ids:
            self.session.add(SprintTask(task_id=task.id, sprint_id=sprint_id))
        
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def update_task(self, task_id: int, update_data: dict) -> Optional[Task]:
        # Handle relations separately
        category_ids = update_data.pop('category_ids', None)
        sprint_ids = update_data.pop('sprint_ids', None)
        
        if update_data:  # Only update if there are fields to update
            await self.session.execute(
                update(Task)
                .where(Task.id == task_id)
                .values(update_data)
            )
        
        # Update relations if provided
        if category_ids is not None:
            await self.session.execute(
                delete(TaskCategory).where(TaskCategory.task_id == task_id)
            )
            for cat_id in category_ids:
                self.session.add(TaskCategory(task_id=task_id, category_id=cat_id))
        
        if sprint_ids is not None:
            await self.session.execute(
                delete(SprintTask).where(SprintTask.task_id == task_id)
            )
            for sprint_id in sprint_ids:
                self.session.add(SprintTask(task_id=task_id, sprint_id=sprint_id))
        
        await self.session.commit()
        return await self.get_task(task_id)

    async def delete_task(self, task_id: int) -> bool:
        result = await self.session.execute(
            delete(Task).where(Task.id == task_id)
        )
        await self.session.commit()
        return result.rowcount > 0