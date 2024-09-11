import sys
import asyncio
from pathlib import Path
from sqlalchemy import create_engine, insert, text

sys.path.append(str(Path(__file__).absolute().parent.parent.parent))
print(sys.path)

from app.config import Config
from app.db import Base, engine, sm
from app.db.models import (
    User, UserType
)



def init_db():
    c_engine = create_engine(Config.DATABASE_URI, echo=True)
    drop_database = '''
        DROP DATABASE IF EXISTS PDSF;
    '''
    create_database = '''
        CREATE DATABASE IF NOT EXISTS PDSF
        DEFAULT CHARACTER SET utf8mb4
        DEFAULT COLLATE utf8mb4_general_ci;
    '''
    with c_engine.connect() as c:
        c.execute(text(drop_database))
        c.execute(text(create_database))
    # c_engine.execute(sql_cmd)


async def init_table():
    async with engine.begin() as cnn:
        await cnn.run_sync(Base.metadata.drop_all)
        await cnn.run_sync(Base.metadata.create_all)
        await init_data()


async def init_data():
    async with sm.begin() as ss:
        password = User.gen_password(Config.PASSWORD)
        await ss.execute(insert(User).values(
            usercount=Config.USERCOUNT, 
            password=password,
            type=UserType.ADMIN,
            )
        )


if __name__ == "__main__":
    init_db()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_table())