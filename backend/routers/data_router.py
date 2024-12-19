import os
import pandas as pd
from fastapi import APIRouter, Depends, UploadFile, Request
from fastapi.exceptions import HTTPException

from config import Config
from db.dao.data_dao import DataDao
from db.schemas.data_schema import DataCreate, DataInfo, DataFilter, SaleData
from utils.depends import DALGetter, LoggedIn, NeedAdmin
from utils.uuid_ import gen_str_uuid1
from utils.depends import NeedAdmin, DALGetter


data_api = APIRouter(prefix="/data",tags=["Data"])


# 初始化文件上传
@data_api.post("/upload_data_file", dependencies=[Depends(NeedAdmin)])
async def upload_data_file(
    file: UploadFile,
    data_dao: DataDao = Depends(DALGetter(DataDao))
):
    # 后缀检查
    fname = file.filename
    *_, suffix = fname.split(".")
    if suffix not in Config.SUFFIXES:
        raise HTTPException(422, f"file suffix must in {Config.SUFFIXES}")
    
    # 保存到本地    
    fpath = Config.UPLOAD_DIR.joinpath(f"{gen_str_uuid1()}.{suffix}")
    with open(fpath, "bw")as f:
        f.write(await file.read())

    # 读取数据准备详细检查
    if suffix == "csv":
        data = pd.read_csv(fpath)
    elif suffix == "xlsx":
        data = pd.read_excel(fpath)
    # 字段检查
    data.columns = [i.lower() for i in data.columns]
    columns = data.columns
    for i in Config.COLUMNS:
        if i not in columns:
            raise HTTPException(422, f"file must contain {Config.COLUMNS} columns")
    data: pd.DataFrame = data[Config.COLUMNS]
    for (c, n), d in data.groupby(["code", "name"]):
        data_ = DataCreate(code=c, name=n)
        data_info = await data_dao.select_or_insert(data_)
        id = data_info.id
        dir_ = Config.RAWDATA_DIR.joinpath(str(id))
        dir_.mkdir(exist_ok=True, parents=True)
        file_path = dir_.joinpath("data.xlsx")
        d[["date", "quantity"]].to_excel(file_path, index=False)
    os.remove(fpath)
    return "ok"


# 增量文件上传
@data_api.post("/increacement_upload_data_file", dependencies=[Depends(NeedAdmin)])
async def increacement_upload_data_file(
    file: UploadFile,
    data_dao: DataDao = Depends(DALGetter(DataDao))
):
    # 后缀检查
    fname = file.filename
    *_, suffix = fname.split(".")
    if suffix not in Config.SUFFIXES:
        raise HTTPException(422, f"file suffix must in {Config.SUFFIXES}")
    
    # 保存到本地    
    fpath = Config.UPLOAD_DIR.joinpath(f"{gen_str_uuid1()}.{suffix}")
    with open(fpath, "bw")as f:
        f.write(await file.read())

    # 读取数据准备详细检查
    if suffix == "csv":
        increacement_data = pd.read_csv(fpath)
    elif suffix == "xlsx":
        increacement_data = pd.read_excel(fpath)
    # 字段检查
    increacement_data.columns = [i.lower() for i in increacement_data.columns]
    columns = increacement_data.columns
    for i in Config.COLUMNS:
        if i not in columns:
            raise HTTPException(422, f"file must contain {Config.COLUMNS} columns")
    increacement_data: pd.DataFrame = increacement_data[Config.COLUMNS]
    for (c, n), d in increacement_data.groupby(["code", "name"]):
        data_ = DataCreate(code=c, name=n)
        data_info = await data_dao.select_or_insert(data_)
        id = data_info.id

        dir_ = Config.RAWDATA_DIR.joinpath(str(id))
        dir_.mkdir(exist_ok=True, parents=True)
        file_path = dir_.joinpath("data.xlsx")
        if file_path.exists():
            old_data = pd.read_excel(file_path)
        else:
            d[["date", "quantity"]].to_excel(file_path, index=False)
            continue
        d = d[["date", "quantity"]]
        new_data = pd.concat(
            [old_data, d], 
            ignore_index=True
        ).drop_duplicates().sort_values("date", ascending=True).reset_index(drop=True)
        new_data.to_excel(file_path, index=False)

    os.remove(fpath)
    return "ok"


# 调用接口上传每日订单汇总数据
@data_api.post("/increase_sale_data", dependencies=[Depends(NeedAdmin)])
async def increase_sale_data(
    daily_sale_datas: SaleData,
    data_dao: DataDao = Depends(DALGetter(DataDao))
):
    
    print(daily_sale_datas)
    js_datas = daily_sale_datas.model_dump()["data"]
    
    increacement_data: pd.DataFrame = pd.DataFrame(js_datas)
    for (c, n), d in increacement_data.groupby(["code", "name"]):
        data_ = DataCreate(code=c, name=n)
        data_info = await data_dao.select_or_insert(data_)
        id = data_info.id

        dir_ = Config.RAWDATA_DIR.joinpath(str(id))
        dir_.mkdir(exist_ok=True, parents=True)
        file_path = dir_.joinpath("data.xlsx")
        if file_path.exists():
            old_data = pd.read_excel(file_path)
        else:
            d[["date", "quantity"]].to_excel(file_path, index=False)
            continue
        d = d[["date", "quantity"]]
        new_data = pd.concat(
            [old_data, d], 
            ignore_index=True
        ).drop_duplicates().sort_values("date", ascending=True).reset_index(drop=True)
        new_data.to_excel(file_path, index=False)

    return "ok"


# 查询全部商品
@data_api.get("/select_all", dependencies=[Depends(NeedAdmin)])
async def select_all(
    data_dao: DataDao = Depends(DALGetter(DataDao))
):
    return await data_dao.select_all()


# 按条件查询商品
@data_api.post("/select_filter", dependencies=[Depends(NeedAdmin)])
async def select_filter(
    filter: DataFilter,
    data_dao: DataDao = Depends(DALGetter(DataDao)),
):
    return await data_dao.select_filter(filter)


# 新增一个商品
@data_api.post("/add_data", dependencies=[Depends(NeedAdmin)])
async def add_data(
    data: DataCreate,
    data_dao: DataDao = Depends(DALGetter(DataDao)),
):
    return await data_dao.add_data(data)


# 更新一个商品
@data_api.post("/update_data", dependencies=[Depends(NeedAdmin)])
async def update_data(
    data: DataInfo,
    data_dao: DataDao = Depends(DALGetter(DataDao)),
):
    return await data_dao.update_data(data)