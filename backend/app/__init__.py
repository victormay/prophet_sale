import colorama
import warnings
from dotenv import load_dotenv
from contextlib import asynccontextmanager

warnings.filterwarnings("ignore")
colorama.init(autoreset=True)
load_dotenv()


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers.prediction_router import load_all_predictor, clear_all_predictor
from routers import init_routers
from config.config import Config
from db.engine import async_engine, async_session


# 服务启动和关闭事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    await load_all_predictor()
    yield
    await clear_all_predictor()


# 初始化
app = FastAPI(title="PBSF Api", lifespan=lifespan)


# 跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],   # 允许所有HTTP方法
    allow_headers=["*"]    # 允许所有请求头
)


# 静态资源和本地存储资源
app.mount("/" + str(Config.STATIC_DIR), StaticFiles(directory=Config.STATIC_DIR), name="static")
Config.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
Config.RAWDATA_DIR.mkdir(parents=True, exist_ok=True)


# 路由绑定
init_routers(app)