from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json


app = FastAPI(
    title="未来信息学院"
)


app.mount("/static", StaticFiles(directory="static"), name="static")


template = Jinja2Templates(directory="templates")


with open("./static/data.json", "r", encoding="utf8")as f:
    NEWS = json.load(f)


@app.get("/")
async def index_():
    url = app.url_path_for("index")
    return RedirectResponse(url=url)


@app.get("/chapter02/school/index.html")
async def index(request: Request):
    return template.TemplateResponse(request=request, name="index.html")


@app.get("/chapter02/school/intr.html")
async def intr(request: Request):
    return template.TemplateResponse(request=request, name="intr.html")


@app.get("/chapter02/school/news.html")
async def news(request: Request):
    news_with_index = [(idx+1, n) for idx, n in enumerate(NEWS)]
    return template.TemplateResponse(request=request, name="news.html", context={"news": news_with_index})


@app.get("/chapter02/school/news{n}.html")
async def newsn(request: Request, n: int):
    print(NEWS[n-1])
    return template.TemplateResponse(request=request, name="newsn.html", context=NEWS[n-1])

