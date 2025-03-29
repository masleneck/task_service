import json
from loguru import logger
from src.services.ddl_service import DDLService
from src.core.database import async_session_maker


class ProjectService:
    """Сервис для обработки событий проекта"""
    
    async def process_project_event(self, message: str) -> bool:
        """
        Обрабатывает событие создания проекта
        Возвращает True при успешной обработке
        """
        try:
            data = json.loads(message)
            project_name = data.get("project_name")
            
            if not project_name:
                raise ValueError("Отсутствует project_name в сообщении")
            
            async with async_session_maker() as session:
                success = await DDLService.create_project_tables(session, project_name)
                if success:
                    await session.commit()
                    logger.info(f"Проект '{project_name}' успешно обработан")
                    return True
                await session.rollback()
                return False
                
        except json.JSONDecodeError:
            logger.error("Невалидный JSON в сообщении")
            return False
        except Exception as e:
            logger.error(f"Ошибка обработки проекта: {str(e)}")
            return False