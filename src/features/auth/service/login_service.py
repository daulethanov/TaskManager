import jwt
from datetime import datetime, timedelta

from src.core.config import cfg
from src.core.database import IDatabase
from src.features.auth.models.user import User
from src.features.auth.repositories.login_repo import LoginRepository
from src.features.auth.shemas.auth_shema import LoginSchema


class LoginService:
    def __init__(self, db: IDatabase):
        self.db = db

    @classmethod
    async def _generate_access_token(cls, user: User):
        to_encode = {"id": str(user.id), "email": user.email}
        expire = datetime.utcnow() + timedelta(hours=10)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cfg.JWT_SECRET_KEY, algorithm=cfg.JWT_ALGORITHM)
        return encoded_jwt

    async def login(self, data: LoginSchema) -> dict and int:
        async def _logic(session):
            repo = LoginRepository(session)
            try:
                user = await repo.login_user(data)
                access_token = await LoginService._generate_access_token(user)
                return 200, {"access_token": access_token}
            except ValueError as e:
                return 401, {"error": e.__str__()}

        return await self.db.provide_session(_logic)

