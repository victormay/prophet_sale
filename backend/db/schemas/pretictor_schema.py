from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Union, Annotated


class PretectArgs(BaseModel):
    id: int
    range: int = Field(7, ge=7, le=30)
    reload: bool = Field(False)


class PConfigBase(BaseModel):
    growth: str = Field("linear")
    n_changepoints: int = Field(25)
    changepoint_range: float = Field(0.8)
    yearly_seasonality: bool = Field(True)
    weekly_seasonality: bool = Field(True)
    daily_seasonality: bool = Field(True)
    seasonality_mode: str = Field("additive")
    seasonality_prior_scale: float = Field(10.0)
    holidays_prior_scale: float = Field(10.0)
    changepoint_prior_scale: float = Field(0.05)
    mcmc_samples: float = Field(0)
    interval_width: float = Field(0.8)
    uncertainty_samples: int = Field(1000)
    scaling: str = Field("absmax")
    holidays_mode: str = Field("additive")


class CreatePConfig(PConfigBase):
    user_id: int


class SelectPConfig(PConfigBase):
    id: int
    user_id: int
    create_time: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')  # 自定义格式化为 'YYYY-MM-DD HH:MM:SS'
        }