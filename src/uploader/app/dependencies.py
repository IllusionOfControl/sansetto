from functools import cache
from typing import Annotated

from app.database import Database
from app.repositories import ImageMetaRepository
from app.services import ImageUploadService
from app.settings import Settings
from app.storages import MinIOStorage, Storage
from fastapi import Depends

__all__ = [
    "get_settings",
    "get_database",
    "get_storage",
    "get_image_upload_service",
    "get_image_meta_repository",
]


@cache
def get_settings() -> Settings:
    return Settings()


@cache
def get_database(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Database:
    return Database(settings.database)


def get_storage(settings: Annotated[Settings, Depends(get_settings)]) -> Storage:
    return MinIOStorage(settings=settings.minio)


def get_image_meta_repository(
    database: Annotated[Settings, : Depends(get_database)],
) -> ImageMetaRepository:
    return ImageMetaRepository(database)


def get_image_upload_service(
    storage: Annotated[Storage, Depends(get_storage)],
    image_meta_repository: Annotated[
        ImageMetaRepository, Depends(get_image_meta_repository)
    ],
) -> ImageUploadService:
    return ImageUploadService(storage, image_meta_repository)
