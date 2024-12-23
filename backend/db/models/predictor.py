from datetime import datetime
from sqlalchemy import types
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from prophet import Prophet

from .base import Base


class PConfig(Base):
    __tablename__ = "predictor_config"
    id: Mapped[int] = mapped_column(primary_key=True)
    growth: Mapped[str] = mapped_column(types.String(16), default="linear")
    n_changepoints: Mapped[int] = mapped_column(default=25)
    changepoint_range: Mapped[float] = mapped_column(default=0.8)
    yearly_seasonality: Mapped[bool] = mapped_column(default=True)
    weekly_seasonality: Mapped[bool] = mapped_column(default=True)
    daily_seasonality: Mapped[bool] = mapped_column(default=True)
    seasonality_mode: Mapped[str] = mapped_column(types.String(16), default="additive")
    seasonality_prior_scale: Mapped[float] = mapped_column(default=10)
    holidays_prior_scale: Mapped[float] = mapped_column(default=10)
    changepoint_prior_scale: Mapped[float] = mapped_column(default=0.05)
    mcmc_samples: Mapped[int] = mapped_column(default=0)
    interval_width: Mapped[float] = mapped_column(default=0.8)
    uncertainty_samples: Mapped[int] = mapped_column(default=1000)
    scaling: Mapped[str] = mapped_column(types.String(16), default="absmax")
    holidays_mode: Mapped[str] = mapped_column(types.String(16), default="additive")
    create_time: Mapped[datetime] = mapped_column(
        types.DATETIME(),
        default=lambda :datetime.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def __repr__(self):
        return f"PConfig(id: {self.id})"
