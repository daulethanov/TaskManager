from fastapi import APIRouter
from starlette.responses import JSONResponse
from src.core.database.interfaces import SQLAlchemyDatabase
from src.features.auth.service.login_service import LoginService
from src.features.auth.shemas.auth_shema import RegisterSchema, LoginSchema
from src.features.auth.service.register_service import RegisterService

auth_router = APIRouter()


@auth_router.post("/sign-up")
async def sign_up(body: RegisterSchema):
    db = SQLAlchemyDatabase()
    service = RegisterService(db)
    code, response = await service.register(body)
    return JSONResponse(content=response, status_code=code)


@auth_router.post("/sign-in")
async def sign_in(body: LoginSchema):
    db = SQLAlchemyDatabase()
    service = LoginService(db)
    code, response = await service.login(body)
    return JSONResponse(content=response, status_code=code)