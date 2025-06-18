import uuid

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.features.auth.models.user import User
from src.features.auth.shemas.auth_shema import RegisterSchema


class RegisterRepository:
    def __init__(self, session):
        self.session = session

    async def create_user(self,  data: RegisterSchema):
        new_user = User(
            id=uuid.uuid4(),
            email=data.email,
            username=data.username
        )
        new_user.generate_password_hash(data.password)
        self.session.add(new_user)
        try:
            await self.session.commit()
            await self.session.refresh(new_user)
            return new_user
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("User with this email or username already exists") from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RuntimeError("Database error during user creation") from e

