import uvicorn
import colorama

from app import app

colorama.init(autoreset=True)


if __name__ == "__main__":
    uvicorn.run(app, port=8848)