from pathlib import Path


class Config:
    ROOT = Path(__file__).absolute().parent.parent

    # auth
    TOKEN_EXPIRE = 60*60
    KEY = "Python No.1!"
    METHOD = "HS256"

    # admin
    USERCOUNT = "admin@pdsf.com"
    PASSWORD = "123456"

    # static
    STATIC_DIR = Path("static")
    UPLOAD_DIR = STATIC_DIR.joinpath("uploads")
    RAWDATA_DIR = STATIC_DIR.joinpath("rawdata")

    # data
    SUFFIXES = ["csv", "xlsx"]
    COLUMNS = ["date", "code", "name", "quantity"]
