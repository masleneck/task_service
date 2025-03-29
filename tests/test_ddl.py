import asyncio
from loguru import logger
from src.core.database import async_session_maker
from src.services.ddl_service import DDLService

TEST_PROJECT = "test_project_123"  # Уникальное имя для теста

async def test_ddl_operations():
    logger.info("=== Начало теста DDL операций ===")
    
    async with async_session_maker() as session:
        # 1. Проверяем, что таблиц нет
        logger.info(f"Проверяем отсутствие таблиц для проекта {TEST_PROJECT}...")
        for table in ["tasks", "categories"]:
            exists = await DDLService.table_exists(session, TEST_PROJECT, table)
            assert not exists, f"Таблица {table} уже существует!"
        
        # 2. Создаем таблицы
        logger.info(f"Создаем таблицы для {TEST_PROJECT}...")
        created = await DDLService.create_project_tables(session, TEST_PROJECT)
        assert created, "Не удалось создать таблицы"
        
        # 3. Проверяем создание
        logger.info("Проверяем созданные таблицы...")
        for table in ["tasks", "categories", "sprints"]:
            exists = await DDLService.table_exists(session, TEST_PROJECT, table)
            assert exists, f"Таблица {table} не создана!"
        
        # 4. Удаляем таблицы
        logger.info(f"Удаляем таблицы {TEST_PROJECT}...")
        deleted = await DDLService.drop_project_tables(session, TEST_PROJECT)
        assert deleted, "Не удалось удалить таблицы"
        
        # 5. Проверяем удаление
        logger.info("Проверяем удаление таблиц...")
        for table in ["tasks", "categories"]:
            exists = await DDLService.table_exists(session, TEST_PROJECT, table)
            assert not exists, f"Таблица {table} не удалена!"
    
    logger.success("=== Все тесты пройдены успешно ===")

if __name__ == "__main__":
    logger.add("ddl_test.log", rotation="1 MB")  # Логи в файл
    asyncio.run(test_ddl_operations())

    # python -m tests.test_ddl