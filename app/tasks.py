from io import BytesIO

from PIL import Image as PillowImage
from telebot import TeleBot

from app.config import Config
from app.extensions import scheduler
from app.main import db
from app.models import Image
from app.storage import ImageStorage


@scheduler.task(
    "interval",
    id="upload_to_telegram",
    max_instances=1,
    minutes=10
)
def upload_to_telegram():
    with scheduler.app.app_context():
        bot = TeleBot(token=Config.TELEGRAM_BOT_TOKEN)
        storage = ImageStorage()

        image = db.session.query(Image).filter_by(is_published=False).first()
        if not image:
            return

        image_data = storage.retrieve(image.filename)

        image_buff = BytesIO(image_data)
        thumbnail_buff = BytesIO()

        thumbnail_image = PillowImage.open(image_buff)
        thumbnail_image.thumbnail((800, 800))
        thumbnail_image.save(thumbnail_buff, format="JPEG")

        bot.send_photo(
            chat_id=Config.TELEGRAM_CHANNEL_ID,
            photo=thumbnail_buff.getvalue(),
        )
        bot.send_document(
            chat_id=Config.TELEGRAM_CHANNEL_ID,
            visible_file_name=Config.TELEGRAM_FILENAME_PATTERN.format(image.id),
            document=image_data
        )

        image.is_published = True
        image.save()
