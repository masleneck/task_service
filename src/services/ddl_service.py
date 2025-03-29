# src/services/ddl_service.py
from sqlalchemy import text
from loguru import logger
from typing import List, Dict
from src.core.database import async_session_maker

class DDLService:
    @classmethod
    def _validate_project_name(cls, project_name: str) -> bool:
        """Валидация имени проекта (только буквы, цифры и подчеркивания)"""
        return (
            isinstance(project_name, str) and 
            project_name.replace('_', '').isalnum() and
            2 <= len(project_name) <= 50
        )

    @classmethod
    def _get_table_definitions(cls, project_name: str) -> List[Dict[str, str]]:
        """Генерация SQL для создания всех таблиц проекта"""
        return [
            {
                "name": "tasks",
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
                "name": "categories",
                "sql": f"""
                    CREATE TABLE IF NOT EXISTS {project_name}_categories (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL UNIQUE
                    )
                """
            },
            {
                "name": "sprints",
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
                "name": "task_categories",
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
                "name": "sprint_tasks",
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
        """Создает все таблицы для нового проекта"""
        if not cls._validate_project_name(project_name):
            logger.error(f"Invalid project name: {project_name}")
            return False

        try:
            # Создаем таблицы в правильном порядке
            tables = cls._get_table_definitions(project_name)
            
            # Сначала основные таблицы
            for table in tables[:3]:  # tasks, categories, sprints
                await session.execute(text(table["sql"]))
            
            # Затем связующие таблицы
            for table in tables[3:]:  # task_categories, sprint_tasks
                await session.execute(text(table["sql"]))
            
            await session.commit()
            logger.success(f"Created tables for project '{project_name}'")
            return True
            
        except Exception as e:
            await session.rollback()
            logger.error(f"Failed to create tables: {str(e)}")
            return False

    @classmethod
    async def drop_project_tables(cls, session, project_name: str) -> bool:
        """Удаляет все таблицы проекта с каскадным удалением"""
        if not cls._validate_project_name(project_name):
            logger.error(f"Invalid project name: {project_name}")
            return False

        try:
            # Удаляем в обратном порядке (сначала связующие)
            tables = cls._get_table_definitions(project_name)
            for table in reversed(tables):
                await session.execute(
                    text(f"DROP TABLE IF EXISTS {project_name}_{table['name']} CASCADE")
                )
            
            await session.commit()
            logger.success(f"Dropped tables for project '{project_name}'")
            return True
            
        except Exception as e:
            await session.rollback()
            logger.error(f"Failed to drop tables: {str(e)}")
            return False

    @classmethod
    async def table_exists(cls, session, project_name: str, table_name: str) -> bool:
        """Проверяет существование таблицы"""
        try:
            result = await session.execute(
                text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = :table_name
                    )
                """), 
                {"table_name": f"{project_name}_{table_name}"}
            )
            return result.scalar()
        except Exception as e:
            logger.error(f"Table check failed: {str(e)}")
            return False