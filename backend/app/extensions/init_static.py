from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from app.config import Config


template = Jinja2Templates(directory=Config.ROOT.joinpath("templates"))


def init_static(app:FastAPI):
    app.mount("/static",StaticFiles(directory=Config.ROOT.joinpath("static")),name="static")
