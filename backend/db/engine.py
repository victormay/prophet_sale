import os
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession
)


DB_URI = os.environ['DB_URI']
DB_NAME = os.environ['DB_NAME']
SYNC_BACKEND = os.environ['SYNC_BACKEND']
ASYNC_BACKEND = os.environ['ASYNC_BACKEND']
ECHO = eval(os.environ["ECHO"])


def build_uri(backend, name=""):
    uri = DB_URI.replace("{engine}", backend)
    uri = uri.replace("{db}", name)
    return uri


async_engine: AsyncEngine = create_async_engine(
    build_uri(ASYNC_BACKEND, DB_NAME),
    pool_pre_ping=True,
    echo=ECHO
)


async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(async_engine)