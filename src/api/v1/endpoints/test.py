from fastapi import APIRouter, HTTPException, Body
from src.kafka.producer import producer
from loguru import logger
from pydantic import BaseModel

class ProjectMessage(BaseModel):
    project_name: str

test_router = APIRouter(prefix="/test", tags=["Test Kafka"])

@test_router.post("/kafka")
async def test_kafka(message: ProjectMessage = Body(...)):
    try:
        message_dict = message.dict()
        logger.debug(f"Sending to Kafka: {message_dict}")
        
        success = await producer.send(
            topic="project_events",
            message=message_dict
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send to Kafka")
            
        return {"status": "ok", "project": message.project_name}
        
    except Exception as e:
        logger.error(f"Test endpoint error: {e}")
        raise HTTPException(status_code=400, detail=str(e))