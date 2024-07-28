from app.dependencies import get_image_publisher_service
from app.logging import logger


async def task_publish_image() -> None:
    logger.info("start task publishing image")
    image_publisher_service = get_image_publisher_service()

    try:
        await image_publisher_service.publish()
    except Exception as exc:
        logger.exception(exc)
    finally:
        logger.info("finish task publishing image")
