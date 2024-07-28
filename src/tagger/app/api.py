from typing import Annotated

from app.dependencies import get_tagger_service
from app.exceptions import InternalException
from app.services import TaggingService
from app.utils import check_accepted_mimetype
from fastapi import APIRouter, Depends, File, UploadFile

router = APIRouter()

TaggingServiceDep = Annotated[TaggingService, Depends(get_tagger_service)]


@router.post("/predict_tags")
def upload(
    image: Annotated[UploadFile, File()],
    tagging_service: TaggingServiceDep,
):
    if not check_accepted_mimetype(image.content_type):
        return {
            "success": False,
            "message": "unsupported content type",
        }

    file_buff = image.file.read()
    try:
        tags = tagging_service.predict_tags(
            image_buff=file_buff,
        )
    except InternalException as exc:
        return {"success": False, "message": str(exc)}
    else:
        return {"success": True, "data": {"tags": tags}}
