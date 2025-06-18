from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from src.core.config import cfg

Base = declarative_base()


engine = create_async_engine(cfg.SQLALCHEMY_DATABASE_URI, echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


def get_async_session() -> AsyncSession:
    return async_session_maker()
