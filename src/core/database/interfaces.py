from src.core.database import IDatabase
from src.core.database.psql import async_session_maker


class SQLAlchemyDatabase(IDatabase):
    async def provide_session(self, func):
        async with async_session_maker() as session:
            return await func(session)
