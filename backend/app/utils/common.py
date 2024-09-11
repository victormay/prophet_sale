from uuid import uuid1
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt, JWTError
from app.config import Config


def current_now():
    return datetime.utcnow()


def gen_uuid():
    return uuid1().__str__()


auth_tool = OAuth2PasswordBearer(tokenUrl="/auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


def gen_token(info: dict, expire: int = Config.TOKEN_EXPIRE):
    exp = current_now() + timedelta(seconds=expire)
    info.update({"exp": exp})
    token = jwt.encode(info,Config.KEY,Config.METHOD)
    return token


def parse_token(token: OAuth2PasswordBearer):
    info = jwt.decode(token, Config.KEY,Config.METHOD)
    return info


async def question_form_web(question):
    op = "ABCDEFGH"
    print(question)
    question["options"] = list(map(lambda x: [op[question["options"].index(x)], x], question["options"]))
    question["answer"] = list(map(lambda x: op[x], question["answer"]))
    print(question)
    return question


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyY291bnQiOiIxNTc2MDA3MDUzNiIsInBhc3N3b3JkIjoiMTIzNDU2IiwiZXhwIjoxNjUyMDY3NzI0fQ.jMlq0P8f40pOrX-2UnKDz6xCeOjCebk1wFerf0ir7IE"
    print(parse_token(token))