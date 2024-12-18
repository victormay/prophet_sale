import pandas as pd
from fastapi import APIRouter, Depends, UploadFile
from fastapi.exceptions import HTTPException

from utils.depends import DALGetter, LoggedIn, NeedAdmin
from utils.uuid_ import gen_str_uuid1
from config import Config


data_api = APIRouter(prefix="/data",tags=["Data"])


@data_api.post("/upload", dependencies=[Depends(NeedAdmin)])
async def update_data(
    file: UploadFile
):
    # 后缀检查
    fname = file.filename
    *_, suffix = fname.split(".")
    if suffix not in Config.SUFFIXES:
        raise HTTPException(422, f"file suffix must in {Config.SUFFIXES}")
    
    # 保存到本地
    root = Config.STATIC_DIR
    upload_dir = root.joinpath("uploads")
    fpath = upload_dir.joinpath(f"{gen_str_uuid1()}.{suffix}")
    with open(fpath, "bw")as f:
        f.write(await file.read())

    # 读取数据准备详细检查
    if suffix == "csv":
        data = pd.read_csv(fpath)
    elif suffix == "xlsx":
        data = pd.read_excel(fpath)

    # 字段检查
    name_map = {}
    columns = [i for i in data.columns]
    lower_columns = [i.lower() for i in data.columns]
    for i in Config.COLUMNS:
        if i not in lower_columns:
            raise HTTPException(422, f"file must contain {Config.COLUMNS} columns")
        else:
            name_map[columns[lower_columns.index(i)]] = i
    data = data.rename(columns=name_map)
    data = data[Config.COLUMNS]

    # TODO 如何保存
    # goods = data["name"].unique()

    # for i in goods:
    #     dt = data[data["name"]==i]
    #     print(dt.shape)
        # dir_ = root.joinpath(nm.replace("*", "").replace(":", "").replace(" ", "_"))
        # dir_.mkdir(parents=True, exist_ok=True)
        # dt.to_excel(dir_.joinpath("data.xlsx"), index=None)
    return "ok"
