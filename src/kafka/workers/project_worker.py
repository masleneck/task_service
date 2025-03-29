from loguru import logger
from src.services.ddl_service import DDLService
from src.core.database import async_session_maker

class ProjectWorker:
    async def handle(self, message: dict) -> bool:
        try:
            async with async_session_maker() as session:
                if message.get("action") == "create_project":
                    return await DDLService.create_project_tables(
                        session,
                        message["project_name"]
                    )
                elif message.get("action") == "delete_project":
                    return await DDLService.drop_project_tables(
                        session,
                        message["project_name"]
                    )
            return False
        except Exception as e:
            logger.error(f"ProjectWorker error: {e}")
            return False