from hashlib import md5
from io import BytesIO

from app.exceptions import InternalException
from app.models import ImagesMetaModel
from app.repositories import ImageMetaRepository
from app.schemas import ImageMetaScheme
from app.storages import Storage
from PIL import Image

__all__ = ["ImageUploadService"]


class ImageUploadService:
    def __init__(
        self,
        storage: Storage,
        image_repo: ImageMetaRepository,
    ):
        self._storage = storage
        self._image_meta_repo = image_repo

    @staticmethod
    async def _generate_thumbnail(file_buff: bytes) -> bytes:
        image = Image.open(BytesIO(file_buff))
        image.thumbnail((600, 600))

        thumb_buff = BytesIO()
        image.save(thumb_buff)
        return thumb_buff.getvalue()

    @staticmethod
    async def _convert_image_to_jpg(image_buff: bytes) -> bytes:
        image = Image.open(BytesIO(image_buff))
        new_image_buff = BytesIO()
        image.save(new_image_buff, "jpg")
        return new_image_buff.getvalue()

    async def upload(self, image_buff: bytes, meta_raw: str) -> None:
        try:
            image_buff = await self._convert_image_to_jpg(image_buff)

            md5_hash = md5(image_buff).hexdigest()

            metadata = ImageMetaScheme.model_validate_json(meta_raw)
            image_meta_model = ImagesMetaModel(
                author=metadata.author,
                source=metadata.source,
                tags=metadata.tags,
                md5=md5_hash,
            )
            await self._image_meta_repo.create(image_meta_model)

            thumbnail_buff = await self._generate_thumbnail(image_buff)
            await self._storage.store(
                f"thumbnails/{image_meta_model.uid.hex}", thumbnail_buff
            )
            await self._storage.store(f"images/{image_meta_model.uid.hex}", image_buff)
        except Exception as exc:
            raise InternalException from exc
