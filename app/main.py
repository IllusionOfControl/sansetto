import logging

from celery import Celery, Task
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import Config
from app.extensions import scheduler

db = SQLAlchemy()


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name)
    celery_app.config_from_object(dict(
        broker_url=Config.CELERY_BROKER_URL,
        result_backend=Config.CELERY_RESULT_BACKEND,
        task_ignore_result=True,
    ))
    celery_app.Task = FlaskTask
    celery_app.set_default()
    app.extensions["celery"] = celery_app

    @celery_app.on_after_configure.connect()
    def setup_periodic_tasks(sender, **kwargs):
        from app.tasks import upload_to_telegram
        sender.add_periodic_task(10, upload_to_telegram, name="Periodic upload to telegram")

    return celery_app


def create_app() -> Flask:
    app = Flask(__name__, static_url_path="/static", static_folder="static/")
    app.config.from_object(Config)

    scheduler.init_app(app)
    logging.getLogger("apscheduler").setLevel(logging.INFO)

    db.init_app(app)
    celery_init_app(app)

    with app.app_context():
        from app import tasks  # noqa: F401

        db.create_all()
        scheduler.start()

    from app.views import bp

    app.register_blueprint(bp)

    return app


app = create_app()
celery = app.extensions["celery"]
