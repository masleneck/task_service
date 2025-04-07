from fastapi import APIRouter
from app.api.endpoints import projects_router

main_router = APIRouter()
main_router.include_router(projects_router)