from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from src.features.auth.models.user import User
from src.features.auth.shemas.auth_shema import LoginSchema


class LoginRepository:
    def __init__(self, session):
        self.session = session

    async def login_user(self, data: LoginSchema):
        try:
            result = await self.session.execute(select(User).filter(User.email == data.email))

            user = result.scalar_one_or_none()
            if user is None:
                raise ValueError("User not found")

            if not user.check_password(data.password):
                raise ValueError("Incorrect password")

            return user

        except SQLAlchemyError:
            await self.session.rollback()
