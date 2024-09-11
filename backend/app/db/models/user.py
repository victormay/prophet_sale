from uuid import uuid1
from passlib.context import CryptContext
from app.db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, SmallInteger, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


def current_now():
    return datetime.now()


def gen_uuid():
    return uuid1().__str__()


passwd_tool = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserType(enum.Enum):
    ADMIN = 0
    USER = 1


class User(Base):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True,autoincrement=True)
    usercount = Column(String(32), unique=True, nullable=False)
    username = Column(String(64), default=gen_uuid, nullable=False)
    password = Column(String(256), nullable=False)
    img = Column(String(256), nullable=False, default="")
    activate = Column(Boolean, nullable=False, default=True)
    type = Column(Enum(UserType), nullable=False, default="USER")
    create_time = Column(DateTime, default=current_now)
    update_time = Column(DateTime, default=current_now)

    @staticmethod
    def gen_password(password):
        hash_password = passwd_tool.hash(password)
        return hash_password

    @staticmethod
    def valid_password(password,hash_password):
        valid = passwd_tool.verify(password,hash_password)
        return valid

    def __repr__(self):
        return f"<{self.id,self.usercount}>"
