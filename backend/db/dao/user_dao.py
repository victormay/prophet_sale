import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple
from fastapi.exceptions import HTTPException

from db.models.user import User, UserType
from db.schemas.user_schema import UserLogin, UserCrate, UserShow, UserBase
from utils.res_code import code_and_msg, PdsfException
from utils.common import gen_token, parse_token


# @code_and_msg(100001, "user count already exist!")
# class UserCountAlreadyExist(PdsfException):
#     ...


# @code_and_msg(100002, "user not exist!")
# class UserCountNotExist(PdsfException):
#     ...


# @code_and_msg(100003, "password error!")
# class UserPasswordError(PdsfException):
#     ...


# @code_and_msg(100004, "you are not master!")
# class UserNotMaster(PdsfException):
#     ...


# @code_and_msg(100005, "you are not active user!")
# class UserNotActivate(PdsfException):
#     ...


class UserDao:
    def __init__(self,ss: AsyncSession):
        self.ss = ss

    async def login(self, user: UserLogin) -> Tuple[dict, UserBase]:
        email = user.email
        password = user.password
        q = await self.ss.execute(select(User).where(User.email == email))
        user_ = q.scalar()
        if user_ is None:
            raise HTTPException(401, "email not found")
        if not User.verify_password(password, user_.password):
            raise HTTPException(401, "password error")
        user_ = UserBase.model_validate(user_)
        info = user_.model_dump_json()
        return gen_token(json.loads(info))

    # async def insert(self, user: UserIn):
    #     await self.unique_check(user)
    #     user.password = User.gen_password(user.password)
    #     db_user = User(**user.__dict__)
    #     self.ss.add(db_user)
    #     await self.ss.commit()
    #     return db_user

    # async def unique_check(self,user:UserIn):
    #     count = user.usercount
    #     count_exist = await self.ss.execute(select(User).filter(User.usercount==count))
    #     if count_exist.scalar() is not None:
    #         raise UserCountAlreadyExist(count)

    # async def get_user_by_count(self, usercount):
    #     db_user = await self.ss.scalar(select(User).filter(User.usercount==usercount))
    #     if db_user is None:
    #         raise UserCountNotExist(usercount)
    #     return db_user

    # async def get_and_valid_user_by_count(self, info):
    #     usercount = info.get("usercount")
    #     password = info.get("password")
    #     db_user = await self.ss.scalar(select(User).filter(User.usercount == usercount))
    #     if db_user is None:
    #         raise UserCountNotExist(usercount)
    #     hash_password = db_user.password
    #     valid = User.valid_password(password,hash_password)
    #     if not valid:
    #         raise UserPasswordError
    #     if not db_user.activate:
    #         raise UserNotActivate(db_user.usercount)
    #     return db_user

    # async def is_master(self, db_user):
    #     if db_user.usercount not in ["15760070536@qq.com",]:
    #         raise UserNotMaster(db_user.usercount)
    #     return db_user
