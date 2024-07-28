from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import EntityNotFoundException
from app.models import ImagesMetaModel

__all__ = ["ImageMetaRepository"]


class ImageMetaRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[AsyncSession]]
    ):
        self._session_factory = session_factory

    async def get_unpublished(self) -> ImagesMetaModel:
        async with self._session_factory() as session:
            statement = (
                select(ImagesMetaModel)
                .where(ImagesMetaModel.published_at.is_(None))
                .limit(1)
            )
            unpublished_images = await session.execute(statement).scalars().first()
            if not unpublished_images:
                raise EntityNotFoundException("unpublished images not found")
            return unpublished_images

    async def get_published_count(self) -> int:
        async with self._session_factory() as session:
            statement = select(func.count(ImagesMetaModel.id)).where(
                ImagesMetaModel.published_at.is_(None)
            )
            unpublished_images = await session.execute(statement).scalar_one()
            if not unpublished_images:
                raise EntityNotFoundException("unpublished images not found")
            return unpublished_images
