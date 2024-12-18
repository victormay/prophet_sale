from pathlib import Path


class Config:
    DATABASE_URI = "mysql+pymysql://root:123456@172.20.0.220:3306"
    SQLALCHEMY_DATABASE_URI = "mysql+aiomysql://root:123456@172.20.0.220:3306/PDSF"
    ROOT = Path(__file__).absolute().parent.parent

    # auth
    TOKEN_EXPIRE = 60*60
    KEY = "Python No.1!"
    METHOD = "HS256"

    # admin
    USERCOUNT = "admin@pdsf.com"
    PASSWORD = "123456"

    # static
    STATIC_DIR = Path("./static")

    # data
    SUFFIXES = ["csv", "xlsx"]
    COLUMNS = ["date", "quantity", "name"]
