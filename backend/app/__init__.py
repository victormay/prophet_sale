import colorama
from dotenv import load_dotenv

colorama.init(autoreset=True)
load_dotenv()


from fastapi import FastAPI
from routers import init_routers


app = FastAPI(title="PBSF Api")
init_routers(app)

# init_static(app)
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
