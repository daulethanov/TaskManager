from fastapi import APIRouter
from src.features.auth.routers.auth_router import auth_router
from src.features.task.routers.task_router import task_router

router = APIRouter()

router.include_router(auth_router, tags=["Authentication"], prefix="/auth")
router.include_router(task_router, tags=["Tasks"], prefix="/task")
