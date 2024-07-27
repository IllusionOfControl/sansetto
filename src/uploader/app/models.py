import uuid
from datetime import datetime

from sqlalchemy import UUID, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

__all__ = ["ImagesMetaModel"]


class ImagesMetaModel(Base):
    __tablename__ = "images_meta"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(unique=True, default=uuid.uuid4)
    author: Mapped[str] = mapped_column(unique=True, nullable=False)
    tags: Mapped[str] = mapped_column(unique=True, nullable=False)
    source: Mapped[str] = mapped_column(unique=True, nullable=False)

    md5: Mapped[str] = mapped_column(nullable=False)

    uploaded_at: Mapped[datetime] = mapped_column(server_default=func.now())
    published_at: Mapped[datetime | None] = mapped_column()

    def __repr__(self):
        return f"<ImagesMetaModel uuid={self.uuid}>"
