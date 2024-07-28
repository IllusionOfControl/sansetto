from pydantic_settings import BaseSettings, SettingsConfigDict


class MinIOSettings(BaseSettings):
    endpoint: str
    access_key: str
    secret_key: str
    bucket: str
    secure: bool


class DatabaseSettings(BaseSettings):
    protocol: str
    host: str
    port: int
    username: str
    password: str
    database: str


class TelegramSettings(BaseSettings):
    telegram_token: str
    channel_id: str


class PublisherSettings(BaseSettings):
    filename_fmt: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
    )

    minio: MinIOSettings
    database: DatabaseSettings
    telegram: TelegramSettings
    publisher: PublisherSettings
