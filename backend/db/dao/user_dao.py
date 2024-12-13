import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple
from fastapi.exceptions import HTTPException

from db.models.user import User
from db.schemas.user_schema import UserLogin, UserCrate, UserShow, UserBase
from utils.common import gen_token, parse_token


class UserDao:
    def __init__(self,ss: AsyncSession):
        self.ss = ss

    async def login(self, user: UserLogin) -> dict:
        email = user.email
        password = user.password
        q = await self.ss.execute(select(User).where(User.email == email))
        user_ = q.scalar()
        if user_ is None:
            raise HTTPException(401, "email not found!")
        if not User.verify_password(password, user_.password):
            raise HTTPException(401, "password error!")
        user_ = UserBase.model_validate(user_)
        info = user_.model_dump_json()
        return gen_token(json.loads(info))

    async def register(self, user: UserCrate):
        await self.unique_check(user)
        user.password = User.gen_password(user.password)
        db_user = User(**user.__dict__)
        self.ss.add(db_user)
        await self.ss.commit()

    async def unique_check(self, user:UserCrate):
        count_exist = await self.ss.execute(select(User).filter(User.email==user.email))
        if count_exist.scalar() is not None:
            raise HTTPException(422, "email existed, please login or try a new one!")
        
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
