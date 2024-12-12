from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Union, Annotated

from db.models import UserType
from .common import PSDFResponse


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCrate(UserLogin):
    ...


class UserBase(BaseModel):
    id: int
    email: EmailStr
    username: str
    img: str
    type: int
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')  # 自定义格式化为 'YYYY-MM-DD HH:MM:SS'
        }


class UserShow(PSDFResponse):
    data: Optional[Union[List[UserBase], UserBase]]