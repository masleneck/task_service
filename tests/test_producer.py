import pytest
from unittest.mock import AsyncMock
from src.kafka.producer import KafkaProducer

@pytest.mark.asyncio
async def test_producer_send():
    mock_producer = AsyncMock()
    producer = KafkaProducer()
    producer._producer = mock_producer
    producer._is_connected = True
    
    result = await producer.send("test_topic", {"key": "value"})
    
    assert result is True
    mock_producer.send_and_wait.assert_awaited_once()