import json
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple
from datetime import datetime
from fastapi.exceptions import HTTPException

from db.models.data import Data
from config import Config
from db.schemas.data_schema import DataInfo, DataCreate, DataFilter


class DataDao:
    def __init__(self, ss: AsyncSession):
        self.ss = ss

    async def add_data(self, data: DataCreate):
        db_data = Data(**data.__dict__)
        db_data.alias = db_data.name
        self.ss.add(db_data)
        await self.ss.flush([db_data])
        return DataInfo.model_validate(db_data)

    async def select_all(self):
        q = await self.ss.execute(select(Data))
        datas = q.scalars().all()
        datas = [DataInfo.model_validate(i) for i in datas]
        return datas
    
    async def select_by_id(self, id) ->DataInfo:
        q = await self.ss.execute(select(Data).where(Data.id==id))
        data = q.scalar()
        data = DataInfo.model_validate(data)
        return data
    
    async def select_filter(self, filter: DataFilter):

        ...

    async def update_data(self, data: DataInfo):
        q = await self.ss.execute(select(Data).where(Data.id==data.id))
        data_ = q.scalar()
        data_.code = data.code
        data_.alias = data.alias
        data_.update_time = datetime.now()
        self.ss.add(data_)
        await self.ss.commit()
        return data

    async def select_or_insert(self, data: DataCreate) ->DataInfo:
        q = await self.ss.execute(select(Data).where(Data.code==data.code and Data.alias==data.name))
        data_ = q.scalar()
        if data_ is None:
            data_ = await self.add_data(data)
        data_ = DataInfo.model_validate(data_)
        return data_