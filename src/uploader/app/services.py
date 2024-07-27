from hashlib import md5

from PIL import Image

from app.exceptions import InternalException
from app.models import Image
from app.models import ImagesMetaModel
from app.repositories import ImageMetaRepository
from app.schemas import ImageMetaScheme
from app.storages import Storage

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
        image = Image.open(file_buff)
        image.thumbnail((600, 600))
        return image.tobytes()

    async def upload(self, image_buff: bytes, meta_raw: str) -> None:
        try:
            md5_hash = md5(image_buff).hexdigest()

            metadata = ImageMetaScheme.model_validate_json(meta_raw)
            image_meta_model = ImagesMetaModel(
                author=metadata.author,
                source=metadata.source,
                tags=metadata.tags,
                md5=md5_hash
            )
            await self._image_meta_repo.create(image_meta_model)

            thumbnail_buff = await self._generate_thumbnail(image_buff)
            await self._storage.store(f"thumbnails/{image_meta_model.uuid.hex}", thumbnail_buff)
            await self._storage.store(f"images/{image_meta_model.uuid.hex}", image_buff)
        except Exception as exc:
            raise InternalException from exc
