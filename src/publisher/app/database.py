import logging
from contextlib import AbstractContextManager, contextmanager
from typing import Callable

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

__all__ = ("Base", "Database")

from app.settings import DatabaseSettings

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    def __init__(self, settings: DatabaseSettings) -> None:
        url_fmt = "{protocol}://{user}:{password}@{host}:{port}/{database}"
        db_url = url_fmt.format(
            protocol=settings.protocol,
            user=settings.user,
            password=settings.password,
            host=settings.host,
            port=settings.port,
            database=settings.database,
        )

        self._engine = create_async_engine(db_url, echo=True)
        self._session_factory = async_scoped_session(
            async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            conn.run_sync(Base.metadata.create_all)

    @contextmanager
    async def session(self) -> Callable[..., AbstractContextManager[AsyncSession]]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()
