from fastapi import HTTPException
from app.models import Task
from app.repositories.base import BaseDAO



class MovieDAO(BaseDAO[Task]):
    model = Task
    