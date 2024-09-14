from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Union, Annotated

from app.db.models import UserType


class UserIn(BaseModel):
    usercount: Annotated[EmailStr, Field("user@pdsf.com")]
    password: Annotated[str, Field("123456", min_length=6, max_length=20)]


class UserBase(BaseModel):
    id: int
    usercount: str
    username: str
    img: str
    activate: bool
    type: UserType
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    status: int
    data: Optional[Union[List[UserBase],UserBase]]
    msg:Optional[str]
