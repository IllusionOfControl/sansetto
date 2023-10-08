import logging

from flask import Flask

from app.config import Config
from app.extensions import scheduler, db


def create_application() -> Flask:
    application = Flask(__name__, static_url_path="/static", static_folder="static/")
    application.config.from_object(Config)

    scheduler.init_app(application)
    logging.getLogger("apscheduler").setLevel(logging.INFO)

    db.init_app(application)

    with application.app_context():
        from application import tasks  # noqa: F401

        db.create_all()
        scheduler.start()

    from app.views import bp

    application.register_blueprint(bp)

    return application


app = create_application()
