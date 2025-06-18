from src.core.database import IDatabase
from src.features.auth.repositories.register_repo import RegisterRepository
from src.features.auth.shemas.auth_shema import RegisterSchema


class RegisterService:
    def __init__(self, db: IDatabase):
        self.db = db

    async def register(self, data: RegisterSchema) -> dict and int :
        async def _logic(session):
            repo = RegisterRepository(session)
            try:
                await repo.create_user(data)
                return 201, {"success": "ok"}
            except ValueError as e:
                return 400, {"error": e.__str__()}

        return await self.db.provide_session(_logic)

