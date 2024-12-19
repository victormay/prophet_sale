from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Union, Annotated


class DataCreate(BaseModel):
    code: str
    name: str


class TimeFilter(BaseModel):
    start: Optional[datetime]
    end: Optional[datetime]


class DataFilter(BaseModel):
    id: Optional[int]
    code: Optional[str]
    alias: Optional[str]
    create_time: Optional[TimeFilter]
    update_time: Optional[TimeFilter]


class DataInfo(BaseModel):
    id: int
    code: str
    name: str
    alias: str
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')  # 自定义格式化为 'YYYY-MM-DD HH:MM:SS'
        }


class SaleBase(BaseModel):
    date: str
    code: str
    name: str
    quantity: int


class SaleData(BaseModel):
    data: List[SaleBase]