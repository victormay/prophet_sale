from dotenv import load_dotenv

load_dotenv()

import asyncio

from db.engine import async_session
from db.dao.user_dao import UserDao
from utils.depends import DALGetter

a = async_session


async def test():
    async with async_session() as session:
        async with session.begin():
            dao = UserDao(session)
            a = await dao.select_all()
            print(a)

asyncio.get_event_loop().run_until_complete(test())