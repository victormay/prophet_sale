import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple
from datetime import datetime
from fastapi.exceptions import HTTPException

from db.models.user import User
from db.schemas.user_schema import UserLogin, UserCrate, UserBase
from utils.common import gen_token, parse_token


class UserDao:
    def __init__(self,ss: AsyncSession):
        self.ss = ss

    async def login(self, user: UserLogin) -> dict:
        print(self.ss)
        email = user.email
        password = user.password
        q = await self.ss.execute(select(User).where(User.email == email))
        user_ = q.scalar()
        if user_ is None:
            raise HTTPException(401, "email not found!")
        print(user_.password, password)
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
        
    async def select_all(self):
        q = await self.ss.execute(select(User))
        users = [UserBase.model_validate(i) for i in q.scalars().all()]
        return users

    async def update_user(self, user: UserBase):
        q = await self.ss.execute(select(User).where(
            User.id == user.id or User.email == user.email
            )
        )
        users = q.scalars().all()
        if len(users) > 1:
             raise HTTPException(422, "email existed, please try a new one!")
        user_ = users[0]

        user_.email = user.email
        user_.username = user.username
        user_.img = user.img
        user_.admin = user.admin
        user_.update_time = datetime.now()
        user = UserBase.model_validate(user_)
        self.ss.add(user_)
        await self.ss.commit()
        return user
    

    async def update_self(self, current_user: UserBase, user: UserBase):
        if current_user.id == user.id:
            return await self.update_user(user)
        else:
            raise HTTPException(401, "you are modifing anthor person")

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
