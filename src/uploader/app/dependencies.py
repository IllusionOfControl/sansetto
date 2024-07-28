from typing import Annotated

from fastapi import Depends

from app.database import Database
from app.repositories import ImageMetaRepository
from app.services import ImageUploadService
from app.settings import Settings
from app.storages import MinIOStorage, Storage

__all__ = [
    "get_settings",
    "get_database",
    "get_storage",
    "get_image_upload_service",
    "get_image_meta_repository",
]


async def get_settings() -> Settings:
    return Settings()


async def get_database(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Database:
    return Database(settings.database)


async def get_storage(settings: Annotated[Settings, Depends(get_settings)]) -> Storage:
    return MinIOStorage(settings=settings.minio)


async def get_image_meta_repository(
    database: Annotated[Settings,: Depends(get_database)],
) -> ImageMetaRepository:
    return ImageMetaRepository(database)


def get_image_upload_service(
    storage: Annotated[Storage, Depends(get_storage)],
    image_meta_repository: Annotated[
        ImageMetaRepository, Depends(get_image_meta_repository)
    ],
) -> ImageUploadService:
    return ImageUploadService(storage, image_meta_repository)
