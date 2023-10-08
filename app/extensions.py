from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

scheduler = APScheduler()
db = SQLAlchemy()
migrate = Migrate()
