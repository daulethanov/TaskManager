import uuid
from typing import Optional

from src.core.database import IDatabase
from src.features.task.repositories.task_repo import TaskRepository
from src.features.task.shemas.task_shema import CreateTaskSchema, TaskSchema, UpdateTaskSchema


class TaskService:
    def __init__(self, db: IDatabase):
        self.db = db

    async def create_task(self, data: CreateTaskSchema, user_id: str) -> dict and int:
        async def _logic(session):
            repo = TaskRepository(session)
            try:
                user_uuid = uuid.UUID(user_id)
                await repo.create_task(data, user_uuid)
                return 201, {"ok": "success"}
            except ValueError as e:
                return 500, {"error": e.__str__()}

        return await self.db.provide_session(_logic)

    async def list_task(self, user_id: str, status: Optional[str] = None) -> tuple[int, dict]:
        async def _logic(session):
            try:
                user_uuid = uuid.UUID(user_id)
                repo = TaskRepository(session)
                tasks = await repo.task_list(user_uuid, status)

                result = [
                    TaskSchema.model_validate(task).model_dump(mode="json") for task in tasks
                ]
                return 200, result

            except ValueError as e:
                return 400, {"error": str(e)}

        return await self.db.provide_session(_logic)

    async def delete_task(self, task_id):
        async def _logic(session):

            repo = TaskRepository(session)
            try:

                message = await repo.delete_task_id(task_id)
                return 201, {"ok": message}
            except ValueError as e:
                return 400, {"error": e.__str__()}
            except Exception as e:
                return 500, {"error": e.__str__()}

        return await self.db.provide_session(_logic)

    async def update_task(self, data: UpdateTaskSchema, task_id: uuid.UUID, user_id: str) -> dict and int:
        async def _logic(session):
            repo = TaskRepository(session)
            try:
                user_uuid = uuid.UUID(user_id)
                await repo.update_task(task_id, data, user_uuid)
                return 201, {"ok": "update"}
            except ValueError as e:
                return 500, {"error": e.__str__()}

        return await self.db.provide_session(_logic)

    async def mark_overdue_tasks(self):
        async def _logic(session):
            repo = TaskRepository(session)
            try:
                await repo.check_date_task()
                return 200, {"ok": "update"}
            except ValueError as e:
                return 500, {"error": e.__str__()}

        return await self.db.provide_session(_logic)
