import os
from distutils.util import strtobool
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALEMBIC_MIGRATE_DIRECTORY = "app/migrations"

    MINIO_HOST = os.environ["MINIO_HOST"]
    MINIO_ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]
    MINIO_SECRET_KEY = os.environ["MINIO_SECRET_KEY"]
    MINIO_SECURE = bool(strtobool(os.environ["MINIO_SECURE"]))
    MINIO_BUCKET = os.environ["MINIO_BUCKET"]

    TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    TELEGRAM_CHANNEL_ID = os.environ["TELEGRAM_CHANNEL_ID"]
    TELEGRAM_FILENAME_PATTERN = os.environ["TELEGRAM_FILENAME_PATTERN"]
