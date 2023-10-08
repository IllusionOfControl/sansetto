import uuid
import hashlib
from io import BytesIO

from flask import Blueprint, request, flash, render_template, redirect, url_for

from PIL import Image as PillowImage
from app.models import Image
from app.storage import ImageStorage

bp = Blueprint("views", __name__)

accepted_mimetypes = [
    "image/jpeg",
    "image/png",
]


@bp.get("/")
def index():
    return render_template("index.html")


@bp.post("/upload_images")
def upload_images():
    files = request.files.getlist("images[]")

    storage = ImageStorage()

    for file in files:
        if file.mimetype not in accepted_mimetypes:
            flash("error", f"File {file.filename} is not accepted.")
            continue

        image_data = file.stream.read()
        # new_filename = uuid.uuid4().hex
        #
        # image_obj = Image(
        #     filename=new_filename,
        #     md5=hashlib.md5(image_data).hexdigest()
        # )
        # image_obj.save()
        #
        # image_buff = BytesIO(image_data)
        # im = PillowImage.open(image_buff)
        # im.save(image_buff, format="JPEG")
        #
        # storage.store(image_buff.getvalue(), image_obj.filename)

    return redirect(url_for("views.index"))
