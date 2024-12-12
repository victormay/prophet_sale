import enum
from sqlalchemy import types
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from utils.uuid_ import gen_str_uuid1
from utils.password import gen_password, verify_password


class UserType(enum.IntEnum):
    ADMIN = 0
    USER = 1


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(types.String(30), unique=True)
    username: Mapped[str] = mapped_column(
        types.String(64),
        default=gen_str_uuid1,
    )
    password: Mapped[str] = mapped_column(types.String(256))
    img: Mapped[str] = mapped_column(types.String(128), default="default.png")
    activate: Mapped[bool] = mapped_column(types.Boolean, default=True)
    type: Mapped[UserType] = mapped_column(default="USER")
    create_time: Mapped[datetime] = mapped_column(
        types.DATETIME(),
        default=lambda :datetime.now()
    )
    update_time: Mapped[datetime] = mapped_column(
        types.DATETIME(),
        default=lambda :datetime.now()
    )

    @staticmethod
    def gen_password(passwd):
        return gen_password(passwd)

    @staticmethod
    def verify_password(passwd, hashed_passwd):
        return verify_password(passwd, hashed_passwd)

    def __repr__(self):
        return f"User(id: {self.id}, usercount: {self.usercount})"