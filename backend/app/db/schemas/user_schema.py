from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Union
from fastapi import Form


class UserIn(BaseModel):
    usercount: EmailStr = Field(...)
    password: str = Field(..., min_length=6)

    @classmethod
    def as_form(cls,
                usercount: EmailStr=Form(...),
                password: str=Form(...,min_length=6)
                ):
        return cls(usercount=usercount,password=password)


class UserBase(BaseModel):
    id: int
    usercount: str
    username: str
    img: str
    activate: bool
    c_time: datetime
    u_time: datetime

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    status: int
    data: Optional[Union[List[UserBase],UserBase]]
    msg:Optional[str]
