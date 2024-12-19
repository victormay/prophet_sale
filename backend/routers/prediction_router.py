import os
import pandas as pd
from fastapi import APIRouter, Depends, UploadFile, Request, Path
from fastapi.exceptions import HTTPException

from config import Config
from db.dao.data_dao import DataDao
from db.schemas.data_schema import DataCreate, DataInfo, DataFilter, SaleData
from utils.depends import DALGetter, LoggedIn, NeedAdmin
from utils.uuid_ import gen_str_uuid1
from utils.depends import NeedAdmin, DALGetter
from utils.predoctor import Predictor


PREDICTORS = []


pred_api = APIRouter(prefix="/pred",tags=["Pred"])


@pred_api.get("/{id}", dependencies=[Depends(LoggedIn)])
async def pred_test(
    id,
    data_dao: DataDao = Depends(DALGetter(DataDao))
):
    data = await data_dao.select_by_id(id)

    if id in PREDICTORS:
        predictor = PREDICTORS[PREDICTORS.index(id)]
    else:
        predictor = Predictor({}, id, data.alias)
        predictor.init()
        PREDICTORS.append(predictor)
    
    data = predictor.predict()
    
    print(data.columns)
    print(data)