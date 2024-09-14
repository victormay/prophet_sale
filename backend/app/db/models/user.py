from uuid import uuid1
from passlib.context import CryptContext
from sqlalchemy import types
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import enum

from .base import Base


passwd_tool = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserType(enum.Enum):
    ADMIN = 0
    USER = 1


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    usercount: Mapped[str] = mapped_column(types.String(30), unique=True)
    username: Mapped[str] = mapped_column(
        types.String(64),
        default=lambda : str(uuid1()),
    )
    password: Mapped[str] = mapped_column(types.String(256))
    img: Mapped[str] = mapped_column(types.String(256), default="")
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
    def gen_password(password):
        hash_password = passwd_tool.hash(password)
        return hash_password

    @staticmethod
    def valid_password(password,hash_password):
        valid = passwd_tool.verify(password,hash_password)
        return valid

    def __repr__(self):
        return f"User(id: {self.id}, usercount: {self.usercount})"