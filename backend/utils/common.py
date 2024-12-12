from uuid import uuid1
from pydantic import BaseModel
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


# import sys
# from pathlib import Path

# sys.path.append(Path(__file__).absolute().parent.parent)
# print(sys.path)

from config import Config


def current_now():
    return datetime.now(timezone.utc)


def gen_uuid():
    return uuid1().__str__()


def fmt_datetime(d):
    return datetime.strftime(d, "%Y-%m-%d %H:%M:%S")


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


def gen_token(info: dict, expire: int = Config.TOKEN_EXPIRE):
    exp = current_now() + timedelta(seconds=expire)
    info.update({"exp": exp})
    token = jwt.encode(info, Config.KEY, Config.METHOD)
    return {
        "token": token,
        "expire_in": fmt_datetime(exp + timedelta(hours=8))
    }


def parse_token(token: OAuth2PasswordBearer):
    info = jwt.decode(token, Config.KEY, Config.METHOD)
    return info



if __name__ == '__main__':
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyY291bnQiOiIxNTc2MDA3MDUzNiIsInBhc3N3b3JkIjoiMTIzNDU2IiwiZXhwIjoxNjUyMDY3NzI0fQ.jMlq0P8f40pOrX-2UnKDz6xCeOjCebk1wFerf0ir7IE"
    print(parse_token(token))