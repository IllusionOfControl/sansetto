from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Response, UploadFile, status

from app.dependencies import get_image_upload_service
from app.exceptions import InternalException
from app.services import ImageUploadService
from app.utils import check_accepted_mimetype

router = APIRouter()

ImageUploadServiceDep = Annotated[ImageUploadService, Depends(get_image_upload_service)]


@router.post("/upload")
async def upload(
        image_upload_service: ImageUploadServiceDep,
        image: Annotated[UploadFile, File()],
        meta: Annotated[str, Form()] = "{}",
):
    if not check_accepted_mimetype(image.content_type):
        return {
            "success": False,
            "message": "unsupported content type",
        }

    file_buff = await image.read()
    try:
        await image_upload_service.upload(
            image_buff=file_buff,
            meta_raw=meta,
        )
    except InternalException as exc:
        return {
            "success": True,
            "message": str(exc),
        }

    return Response(status_code=status.HTTP_201_CREATED)
