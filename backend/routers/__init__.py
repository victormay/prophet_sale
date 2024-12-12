from fastapi import FastAPI

from .user_router import user_api

def init_routers(app: FastAPI):
    app.include_router(user_api)