from typing import Annotated
from functools import cache

from fastapi import Depends
from onnxruntime import InferenceSession

from app.logging import logger
from app.services import TaggingService
from app.settings import Settings

__all__ = [
    "get_settings",
    "get_model_session",
    "get_tags_from_model_metadata",
    "get_tagger_service",
]


@cache
def get_settings() -> Settings:
    return Settings()


@cache
def get_model_session() -> InferenceSession:
    logger.info("loading model session")
    tagger_model_path = "models/deepdanbooru-2021.onnx"
    return InferenceSession(tagger_model_path, providers=['CPUExecutionProvider'])


def get_tags_from_model_metadata(
        model_session: Annotated[InferenceSession, Depends(get_model_session)],
) -> list[str]:
    tagger_model_meta = model_session.get_modelmeta().custom_metadata_map
    return eval(tagger_model_meta['tags'])


def get_tagger_service(
        model_session: Annotated[InferenceSession, Depends(get_model_session)],
        tags_list: Annotated[list[str], Depends(get_tags_from_model_metadata)],
) -> TaggingService:
    return TaggingService(
        model_session,
        tags_list
    )
