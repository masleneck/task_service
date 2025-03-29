# модуль для управления DDL (Data Definition Language)

from sqlalchemy import text
from loguru import logger
from typing import List, Dict
from src.core.database import async_session_maker

class DDLService:
    @classmethod
    def _validate_project_name(cls, project_name: str) -> bool:
        """Валидация имени проекта"""
        return (
            isinstance(project_name, str) and 
            project_name.replace('_', '').isalnum() and
            2 <= len(project_name) <= 50
        )

    @classmethod
    def _get_table_definitions(cls, project_name: str) -> List[Dict[str, str]]:
        """Генерация SQL для создания таблиц"""
        return [
            {
                "name": f"{project_name}_tasks",
                "sql": f"""
                    CREATE TABLE IF NOT EXISTS {project_name}_tasks (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        difficulty INTEGER DEFAULT 1,
                        description VARCHAR(1000),
                        status VARCHAR(20) NOT NULL DEFAULT 'TODO',
                        type VARCHAR(20) NOT NULL DEFAULT 'TASK',
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP,
                        ended_at TIMESTAMP,
                        author_id VARCHAR(36) NOT NULL,
                        doer_id VARCHAR(36),
                        parent_id VARCHAR(36)
                    )
                """
            },
            {
                "name": f"{project_name}_categories",
                "sql": f"""
                    CREATE TABLE IF NOT EXISTS {project_name}_categories (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL UNIQUE
                    )
                """
            },
            {
                "name": f"{project_name}_sprints",
                "sql": f"""
                    CREATE TABLE IF NOT EXISTS {project_name}_sprints (
                        id SERIAL PRIMARY KEY,
                        start_date TIMESTAMP NOT NULL,
                        end_date TIMESTAMP,
                        purpose TEXT,
                        is_active BOOLEAN DEFAULT TRUE
                    )
                """
            },
            {
                "name": f"{project_name}_task_categories",
                "sql": f"""
                    CREATE TABLE IF NOT EXISTS {project_name}_task_categories (
                        task_id INTEGER NOT NULL,
                        category_id INTEGER NOT NULL,
                        PRIMARY KEY (task_id, category_id),
                        FOREIGN KEY (task_id) REFERENCES {project_name}_tasks(id) ON DELETE CASCADE,
                        FOREIGN KEY (category_id) REFERENCES {project_name}_categories(id) ON DELETE CASCADE
                    )
                """
            },
            {
                "name": f"{project_name}_sprint_tasks",
                "sql": f"""
                    CREATE TABLE IF NOT EXISTS {project_name}_sprint_tasks (
                        task_id INTEGER NOT NULL,
                        sprint_id INTEGER NOT NULL,
                        PRIMARY KEY (task_id, sprint_id),
                        FOREIGN KEY (task_id) REFERENCES {project_name}_tasks(id) ON DELETE CASCADE,
                        FOREIGN KEY (sprint_id) REFERENCES {project_name}_sprints(id) ON DELETE CASCADE
                    )
                """
            }
        ]

    @classmethod
    async def create_project_tables(cls, session, project_name: str) -> bool:
        """Асинхронное создание таблиц с обработкой ошибок"""
        if not cls._validate_project_name(project_name):
            logger.error(f"Invalid project name format: {project_name}")
            return False

        try:
            for table in cls._get_table_definitions(project_name):
                await session.execute(text(table["sql"]))
            
            logger.success(f"Successfully created tables for project '{project_name}'")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create tables for '{project_name}': {str(e)}")
            await session.rollback()
            return False