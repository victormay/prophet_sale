from datetime import datetime
from sqlalchemy import types
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Data(Base):
    __tablename__ = "data"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(types.String(32))
    name: Mapped[str] = mapped_column(types.String(32), index=True)
    alias: Mapped[str] = mapped_column(types.String(32), index=True, default="")
    create_time: Mapped[datetime] = mapped_column(
        types.DATETIME(),
        default=lambda :datetime.now()
    )
    update_time: Mapped[datetime] = mapped_column(
        types.DATETIME(),
        default=lambda :datetime.now()
    )

    def __repr__(self):
        return f"User(id: {self.id})"