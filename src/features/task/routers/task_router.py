import asyncio
import uuid
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from src.core.database.interfaces import SQLAlchemyDatabase
from src.core.middleware import user_middleware
from src.features.task.services.task_service import TaskService
from src.features.task.shemas.task_shema import CreateTaskSchema, UpdateTaskSchema
from typing import Optional

from src.features.task.task_scheduler import periodic_task_check

task_router = APIRouter()


@task_router.on_event("startup")
async def startup_event():
    db = SQLAlchemyDatabase()
    service = TaskService(db)
    asyncio.create_task(periodic_task_check(service))


@task_router.post("/create")
async def task_create(body: CreateTaskSchema, params: dict = Depends(user_middleware)):
    user_id = params["id"]
    db = SQLAlchemyDatabase()
    service = TaskService(db)
    code, response = await service.create_task(body, user_id)
    return JSONResponse(content=response, status_code=code)


@task_router.get("/list/")
async def task_list(status: Optional[str] = None, params: dict = Depends(user_middleware)):
    user_id = params["id"]
    db = SQLAlchemyDatabase()
    service = TaskService(db)
    code, response = await service.list_task(user_id, status)
    return JSONResponse(content=response, status_code=code)


@task_router.delete("/delete/{task_id}")
async def task_delete(task_id: uuid.UUID, params: dict = Depends(user_middleware)):
    db = SQLAlchemyDatabase()
    service = TaskService(db)
    code, response = await service.delete_task(task_id)
    return JSONResponse(content=response, status_code=code)


@task_router.put("/update/{task_id}")
async def task_update(body: UpdateTaskSchema, task_id: uuid.UUID, params: dict = Depends(user_middleware)):
    db = SQLAlchemyDatabase()
    user_id = params["id"]
    service = TaskService(db)
    code, response = await service.update_task(body, task_id, user_id)
    return JSONResponse(content=response, status_code=code)
