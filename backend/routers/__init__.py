from fastapi import FastAPI

from .user_router import user_api
from .data_router import data_api
from .prediction_router import pred_api

def init_routers(app: FastAPI):
    app.include_router(user_api)
    app.include_router(data_api)
    app.include_router(pred_api)