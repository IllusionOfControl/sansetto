from contextlib import AbstractContextManager
from typing import Callable

from app.models import ImagesMetaModel
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = ["ImageMetaRepository"]


class ImageMetaRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[AsyncSession]]
    ):
        self._session_factory = session_factory

    async def create(self, image_meta: ImagesMetaModel) -> None:
        async with self._session_factory() as session:
            session.add(image_meta)
            await session.commit()
            await session.refresh(image_meta)
