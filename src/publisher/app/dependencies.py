from functools import cache

from app.database import Database
from app.repositories import ImageMetaRepository
from app.services import ImagePublisherService, TelegramService
from app.settings import Settings
from app.storages import MinIOStorage, Storage

__all__ = [
    "get_settings",
    "get_database",
    "get_storage",
    "get_image_meta_repository",
    "get_telegram_service",
    "get_image_publisher_service",
]


@cache
def get_settings() -> Settings:
    return Settings()


@cache
def get_database(
    settings: Settings = get_settings(),
) -> Database:
    return Database(settings.database)


def get_storage(settings: Settings = get_settings()) -> Storage:
    return MinIOStorage(settings=settings.minio)


def get_image_meta_repository(
    database: Database = get_database(),
) -> ImageMetaRepository:
    return ImageMetaRepository(database.session)


def get_telegram_service(settings: Settings = get_settings()) -> TelegramService:
    return TelegramService(settings.telegram)


def get_image_publisher_service(
    settings: Settings = get_settings(),
    storage: Storage = get_storage(),
    image_meta_repository: ImageMetaRepository = get_image_meta_repository(),
    image_publisher_service: TelegramService = get_telegram_service(),
) -> ImagePublisherService:
    return ImagePublisherService(
        storage,
        image_meta_repository,
        image_publisher_service,
        settings.publisher.filename_fmt,
    )
