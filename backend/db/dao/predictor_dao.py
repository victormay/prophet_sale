import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple, List
from datetime import datetime
from fastapi.exceptions import HTTPException

from db.models.predictor import PConfig
from db.schemas.pretictor_schema import CreatePConfig, SelectPConfig, PConfigBase
from db.schemas.user_schema import UserBase


class PredictorDao:
    def __init__(self, ss: AsyncSession):
        self.ss = ss

    async def add_one(self, user: UserBase, cfg: PConfigBase) ->SelectPConfig:
        cpc = PConfig(user_id=user.id, **cfg.__dict__)
        self.ss.add(cpc)
        await self.ss.flush([cpc])
        return SelectPConfig.model_validate(cpc)
    
    async def get_latest(self) ->SelectPConfig:
        q = await self.ss.execute(select(PConfig).order_by(-PConfig.create_time))
        latest_cpc = q.scalars().first()
        return SelectPConfig.model_validate(latest_cpc)
    
    async def get_all(self) ->List[SelectPConfig]:
        q = await self.ss.execute(select(PConfig).order_by(-PConfig.create_time))
        latest_cpces = q.scalars()
        return [SelectPConfig.model_validate(i) for i in latest_cpces]