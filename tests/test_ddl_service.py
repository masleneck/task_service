import pytest
from unittest.mock import AsyncMock
from src.services.ddl_service import DDLService

@pytest.mark.asyncio
async def test_valid_project_name():
    """Тест валидации корректного имени проекта"""
    assert DDLService._validate_project_name("valid_project") is True
    assert DDLService._validate_project_name("invalid!project") is False
    assert DDLService._validate_project_name("a") is False  # Слишком короткое
    assert DDLService._validate_project_name("a" * 51) is False  # Слишком длинное

@pytest.mark.asyncio
async def test_create_tables_success():
    """Тест успешного создания таблиц"""
    mock_session = AsyncMock()
    mock_session.execute.return_value = None
    
    result = await DDLService.create_project_tables(mock_session, "valid_project")
    
    assert result is True
    assert mock_session.execute.call_count == 5
    mock_session.commit.assert_not_awaited()  # commit должен вызываться в вызывающем коде

@pytest.mark.asyncio
async def test_create_tables_failure():
    """Тест обработки ошибок БД"""
    mock_session = AsyncMock()
    mock_session.execute.side_effect = Exception("DB error")
    
    result = await DDLService.create_project_tables(mock_session, "valid_project")
    
    assert result is False
    mock_session.rollback.assert_awaited_once()