from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from app.models import TaskStatus, TaskType


class TaskBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    type: TaskType = Field(default=TaskType.TASK)
    difficulty: int = Field(default=1, ge=1, le=10)
    author_id: str = Field(..., min_length=36, max_length=36)  # UUID validation
    doer_id: Optional[str] = Field(None, min_length=36, max_length=36)
    parent_id: Optional[str] = Field(None, min_length=36, max_length=36)

class TaskCreate(TaskBase):
    category_ids: List[int] = Field(default_factory=list)
    sprint_ids: List[int] = Field(default_factory=list)

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    ended_at: Optional[datetime]
    is_active: bool
    model_config = ConfigDict(from_attributes=True)