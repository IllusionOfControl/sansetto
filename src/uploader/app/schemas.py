from pydantic import BaseModel

__all__ = ["ImageMetaScheme"]


class ImageMetaScheme(BaseModel):
    author: str = ""
    source: str = ""
    tags: str = ""
