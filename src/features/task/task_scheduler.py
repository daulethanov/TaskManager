import asyncio
from src.features.task.services.task_service import TaskService


async def periodic_task_check(service: TaskService):
    while True:
        await service.mark_overdue_tasks()
        await asyncio.sleep(60)
