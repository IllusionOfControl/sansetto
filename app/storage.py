import io
from typing import Any

from minio import Minio

from app.config import Config


class ImageStorage:
    def __init__(self):
        self.minio = self._get_minio_connection()
        self.bucket = Config.MINIO_BUCKET

    @staticmethod
    def _get_minio_connection() -> Minio:
        endpoint = Config.MINIO_HOST
        access_key = Config.MINIO_ACCESS_KEY
        secret_key = Config.MINIO_SECRET_KEY
        secure = Config.MINIO_SECURE

        client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )

        return client

    def store(self, data: bytes, filename: str):
        self.minio.put_object(self.bucket, filename, io.BytesIO(data), len(data))
        return filename

    def delete(self, filename) -> bool:
        self.minio.remove_object(self.bucket, filename)
        return True

    def retrieve(self, filename) -> bytes:
        response = self.minio.get_object(self.bucket, filename)
        data = response.read()

        response.close()
        response.release_conn()

        return data
