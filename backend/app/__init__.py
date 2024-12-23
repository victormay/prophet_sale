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

