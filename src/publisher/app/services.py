from app.exceptions import InternalException
from app.logging import logger
from app.repositories import ImageMetaRepository
from app.settings import TelegramSettings
from app.storages import Storage
from telebot import TeleBot

__all__ = ["TelegramService", "ImagePublisherService"]


class TelegramService:
    def __init__(self, settings: TelegramSettings) -> None:
        self._bot = TeleBot(token=settings.telegram_token)
        self._channel_id = settings.channel_id

    async def publish_image(self, image_buff: bytes, filename: str) -> None:
        logger.info(f"publishing image")
        self._bot.send_document(
            chat_id=self._channel_id, visible_file_name=filename, document=image_buff
        )

    async def publish_thumbnail(self, thumbnail_buff: bytes) -> None:
        logger.info(f"publishing thumbnail")
        self._bot.send_photo(
            chat_id=self._channel_id,
            photo=thumbnail_buff,
        )


class ImagePublisherService:
    def __init__(
        self,
        storage: Storage,
        image_repo: ImageMetaRepository,
        telegram_service: TelegramService,
        filename_fmt: str,
    ):
        self._storage = storage
        self._image_meta_repo = image_repo
        self._telegram_service = telegram_service
        self._filename_fmt = filename_fmt

    async def publish(self) -> None:
        try:
            image_metadata = await self._image_meta_repo.get_unpublished()
            logger.info(f"retrieved unpublished image metadata: {image_metadata}")

            thumbnail_buff = await self._storage.retrieve(
                f"thumbnails/{image_metadata.uuid}"
            )
            image_buff = await self._storage.retrieve(f"images/{image_metadata.uuid}")
            logger.debug("successfully retrieved image and thumbnail buffers")

            published_count = await self._image_meta_repo.get_published_count()
            filename = self._filename_fmt.format(published_count + 1)
            logger.info(f"publishing image '{filename}'...")

            await self._telegram_service.publish_image(image_buff, filename)
            await self._telegram_service.publish_thumbnail(thumbnail_buff)
        except Exception as exc:
            raise InternalException from exc
