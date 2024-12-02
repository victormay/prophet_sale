from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from config import Config


def init_static(app:FastAPI):
    app.mount("/static",StaticFiles(directory=Config.ROOT.joinpath("static")), name="static")
