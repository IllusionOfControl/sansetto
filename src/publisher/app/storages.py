import io

from app.settings import MinIOSettings
from minio import Minio

__all__ = ["Storage", "MinIOStorage"]


class Storage:
    async def store(self, path: str, data: bytes) -> None:
        raise NotImplementedError

    async def delete(self, path: str) -> None:
        raise NotImplementedError

    async def retrieve(self, path: str) -> bytes:
        raise NotImplementedError


class MinIOStorage(Storage):
    def __init__(self, settings: MinIOSettings):
        self._access_key = settings.access_key
        self._secret_key = settings.secret_key
        self._endpoint = settings.endpoint
        self._bucket = settings.bucket
        self._secure = settings.secure

        self._client = Minio(
            self._endpoint,
            access_key=self._access_key,
            secret_key=self._secret_key,
            secure=self._secure,
        )

    async def store(
        self,
        path: str,
        data: bytes,
    ):
        self._client.put_object(self._bucket, path, io.BytesIO(data), len(data))
        return path

    async def delete(self, path: str) -> bool:
        self._client.remove_object(self._bucket, path)
        return True

    async def retrieve(self, path: str) -> bytes:
        response = self._client.get_object(self._bucket, path)
        try:
            data = response.read()
        finally:
            response.close()
            response.release_conn()

        return data
