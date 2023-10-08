from sqlalchemy.sql import func

from app.extensions import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, unique=True, nullable=False)
    md5 = db.Column(db.String(32))
    uploaded_at = db.Column(db.DateTime, server_default=func.now())
    is_published = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
