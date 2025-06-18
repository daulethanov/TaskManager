import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from src.core.config.logging import logger
from src.features.task.models.tag import Tag
from src.features.task.models.task import Task, TaskStatus
from src.features.task.shemas.task_shema import CreateTaskSchema, UpdateTaskSchema


class TaskRepository:
    def __init__(self, session):
        self.session = session

    async def create_task(self, data: CreateTaskSchema, user_id: uuid.UUID):
        naive_due_date = data.due_date.replace(tzinfo=None)

        new_task = Task(
            id=uuid.uuid4(),
            title=data.title,
            description=data.description,
            status=data.status,
            due_date=naive_due_date,
            user_id=user_id
        )

        tags_to_attach = []
        if data.tags:
            for tag_name in data.tags:
                result = await self.session.execute(
                    select(Tag).where(Tag.name == tag_name)
                )
                tag = result.scalar_one_or_none()

                if not tag:
                    tag = Tag(id=uuid.uuid4(), name=tag_name)
                    self.session.add(tag)
                    await self.session.flush()

                tags_to_attach.append(tag)

        new_task.tags = tags_to_attach
        self.session.add(new_task)

        try:
            await self.session.commit()
            await self.session.refresh(new_task)
            return new_task
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RuntimeError(f"Database error during task creation: {str(e)}") from e

    async def task_list(self, user_id, status: Optional[str] = None):
        async with self.session as session:
            query = (
                select(Task)
                .options(selectinload(Task.tags))
                .where(Task.user_id == user_id)
            )

            if status:
                query = query.where(Task.status == TaskStatus(status))

            result = await session.execute(query)
            tasks = result.scalars().all()

            return tasks

    async def delete_task_id(self, task_id: uuid.UUID):
        try:
            query = select(Task).where(Task.id == task_id)
            result = await self.session.execute(query)
            task = result.scalar_one_or_none()

            if task is None:
                raise ValueError("Task not found")

            await self.session.delete(task)
            await self.session.commit()

            return "Task deleted successfully"

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"Database error: {str(e)}")

    async def update_task(self, task_id: uuid.UUID, data: UpdateTaskSchema, user_id: uuid.UUID):
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return None, "Task not found"

        if data.title is not None and data.title.strip() != "":
            task.title = data.title

        if data.description is not None and data.description.strip() != "":
            task.description = data.description

        if data.status is not None and data.status.strip() != "":
            try:
                task.status = TaskStatus(data.status)
            except ValueError:
                return None, f"Invalid status. Must be one of {[s.value for s in TaskStatus]}"

        if data.due_date is not None:
            task.due_date = data.due_date.replace(tzinfo=None)

        try:
            await self.session.commit()
            await self.session.refresh(task)
            return task, None
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RuntimeError(f"Database error during task update: {e}")

    async def check_date_task(self):
        select_stmt = select(Task).where(
            Task.due_date < datetime.utcnow(),
            Task.status != TaskStatus.done,
            Task.status != TaskStatus.overdue
        )
        result = await self.session.execute(select_stmt)
        overdue_tasks = result.scalars().all()

        if overdue_tasks:
            for task in overdue_tasks:
                logger.info(f"Задача '{task.title}' (id={str(task.id)}) стала просроченной.")

            update_stmt = (
                update(Task)
                .where(
                    Task.due_date < datetime.utcnow(),
                    Task.status != TaskStatus.done,
                    Task.status != TaskStatus.overdue
                )
                .values(status=TaskStatus.overdue)
            )
            await self.session.execute(update_stmt)
            await self.session.commit()