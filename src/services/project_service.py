import json
from loguru import logger
from src.services.ddl_service import DDLService
from src.core.database import async_session_maker


class ProjectService:
    """Сервис для обработки событий проекта"""
    
    async def process_project_event(self, message: str) -> bool:
        try:
            data = json.loads(message)
            project_name = data.get("project_name") or data.get("data")  # Ищем в обоих полях
            
            if not project_name:
                logger.warning(f"Invalid message format: {message}")
                return False
                
            async with async_session_maker() as session:
                success = await DDLService.create_project_tables(session, str(project_name))
                if success:
                    await session.commit()
                    logger.info(f"Created tables for project: {project_name}")
                    return True
                    
            return False
        except Exception as e:
            logger.error(f"Project processing error: {str(e)}")
            return False