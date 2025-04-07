import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Импорт всех базовых моделей, чтобы Alembic их видел
from app.models.task import Task, TaskStatus, TaskType
from app.models.category import Category
from app.models.task_category import TaskCategory
from app.models.sprint import Sprint
from app.models.sprint_task import SprintTask
from app.core.database import Base, DATABASE_URL 

# Указываем Alembic, какой URL использовать для подключения к базе данных
config = context.config
config.set_main_option('sqlalchemy.url', DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем Alembic, где искать информацию о моделях. 
# Для этого присваиваем переменной target_metadata метаданные из Base, которые включают все модели
# Эти шаги подготавливают файл env.py к работе с вашей базой данных. 
# Когда мы задаем target_metadata, Alembic получает доступ к структуре всех наших моделей и использует их 
# для создания или обновления схемы базы данных, добавляя новые таблицы и столбцы при изменении моделей.
# Таким образом, файл env.py становится связующим звеном между моделями SQLAlchemy и миграциями в Alembic,
# позволяя легко вносить и отслеживать изменения в базе данных.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()