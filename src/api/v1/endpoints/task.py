from fastapi import APIRouter, Depends, HTTPException
from src.services.task import TaskService
from src.kafka.producer import KafkaProducer
from src.models.task import TaskCreate, TaskRead

router = APIRouter(prefix="/{project_name}/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead)
async def create_task(
    project_name: str,
    task_data: TaskCreate,
    producer: KafkaProducer = Depends(KafkaProducer)
):
    # Отправляем событие в Kafka
    await producer.send(
        topic="task_events",
        value={
            "event_type": "task_create",
            "project_name": project_name,
            "task_data": task_data.dict()
        }
    )
    return {"status": "Task creation initiated"}