from abc import ABC, abstractmethod
from typing import Callable, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession
from .psql import Base


class IDatabase(ABC):
    @abstractmethod
    async def provide_session(self, func: Callable[[AsyncSession], Awaitable]):
        pass
