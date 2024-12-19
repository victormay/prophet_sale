import colorama
from dotenv import load_dotenv

colorama.init(autoreset=True)
load_dotenv()


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import init_routers
from config.config import Config


app = FastAPI(title="PBSF Api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],   # 允许所有HTTP方法
    allow_headers=["*"]    # 允许所有请求头
)


app.mount("/" + str(Config.STATIC_DIR), StaticFiles(directory=Config.STATIC_DIR), name="static")
Config.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
Config.RAWDATA_DIR.mkdir(parents=True, exist_ok=True)

init_routers(app)

#
#
# @app.api_route("/",tags=["Index"],methods=["GET","POST"])
# async def index_page(request:Request):
#     return template.TemplateResponse("index.html",{"request":request})
#
#
# @app.api_route("/test_as",tags=["Index"])
# async def main():
#     from app.db.config import sm
#     from sqlalchemy import text
#     ss = sm()
#     async def test1():
#         print("1")
#         print("2")
#         sql = "show tables;"
#
#         res = await ss.execute(text(sql))
#         print("3")
#         print(res)
#
#     async def test2():
#         print("4")
#         print("5")
#         sql = "show tables;"
#
#         res = await ss.execute(text(sql))
#         print("6")
#         print(res)
#
#     await asyncio.gather(
#         test1(),
#         test2(),
#         return_exceptions=True
#     )
#
