import os
from distutils.util import strtobool


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")

    MINIO_HOST = os.environ.get("MINIO_HOST")
    MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = bool(strtobool(os.environ.get("MINIO_SECURE")))
    MINIO_BUCKET = os.environ.get("MINIO_BUCKET")

    TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    TELEGRAM_CHANNEL_ID = os.environ["TELEGRAM_CHANNEL_ID"]
    TELEGRAM_FILENAME_PATTERN = "Sansetto {}.jpg"
