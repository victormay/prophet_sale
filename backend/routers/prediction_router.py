import os
import pandas as pd
from fastapi import APIRouter, Depends, UploadFile, Request, Path
from fastapi.exceptions import HTTPException
from typing import List

from config import Config
from db.engine import async_session
from db.dao.data_dao import DataDao
from db.schemas.data_schema import DataInfo
from db.dao.predictor_dao import PredictorDao
from db.schemas.pretictor_schema import PretectArgs, PConfigBase
from db.schemas.user_schema import UserBase
from utils.depends import DALGetter, LoggedIn, NeedAdmin
from utils.uuid_ import gen_str_uuid1
from utils.depends import NeedAdmin, DALGetter
from utils.predoctor import Predictor


PREDICTORS: List[Predictor] = []


pred_api = APIRouter(prefix="/pred",tags=["Pred"])


async def load_all_predictor():
    async with async_session() as session:
        async with session.begin():
            data_dao: DataDao = DataDao(session)
            dirs = [i for i in Config.RAWDATA_DIR.glob("*")]
            for i in dirs:
                data = await data_dao.select_by_id(int(i.stem))
                predictor = Predictor({}, data.id, data.alias)
                predictor.init()
                PREDICTORS.append(predictor)


async def reload_all_predictor():
     for i in PREDICTORS:
         i.reload()


async def clear_all_predictor():
    PREDICTORS.clear()


@pred_api.post("/pred_one_sku", dependencies=[Depends(LoggedIn)])
async def pred_one_sku(
    args: PretectArgs,
    data_dao: DataDao = Depends(DALGetter(DataDao))
):
    data: DataInfo = await data_dao.select_by_id(args.id)

    if args.id in PREDICTORS:
        predictor: Predictor = PREDICTORS[PREDICTORS.index(args.id)]
        if args.reload:
            predictor.reload()
    else:
        predictor = Predictor({}, data.id, data.alias)
        predictor.init()
        PREDICTORS.append(predictor)
    
    data = predictor.predict(args.range)
    
    return data.to_dict()


@pred_api.post("/add_pconfig", dependencies=[Depends(LoggedIn)])
async def add_pconfig(
    pconfig: PConfigBase,
    user: UserBase = Depends(LoggedIn),
    p_dao: PredictorDao = Depends(DALGetter(PredictorDao))
):
    return await p_dao.add_one(user, pconfig)


@pred_api.get("/get_latest_pconfig", dependencies=[Depends(LoggedIn)])
async def get_latest_pconfig(
    p_dao: PredictorDao = Depends(DALGetter(PredictorDao))
):
    return await p_dao.get_latest()


@pred_api.get("/get_all", dependencies=[Depends(LoggedIn)])
async def get_latest_pconfig(
    p_dao: PredictorDao = Depends(DALGetter(PredictorDao))
):
    return await p_dao.get_all()