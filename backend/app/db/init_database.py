import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).absolute().parent.parent.parent))
load_dotenv()

from app.db.models import *
from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session
from engine import build_uri, SYNC_BACKEND, DB_NAME, ECHO


USER_COUNT = os.environ["USER_COUNT"]
PASSWORD = os.environ["PASSWORD"]



def init_db():
    engine = create_engine(
        build_uri(SYNC_BACKEND),
        echo=ECHO
    )
    drop_database = "DROP DATABASE IF EXISTS PDSF;"
    create_database = ("CREATE DATABASE IF NOT EXISTS PDSF "
                       "DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci;")
    with engine.connect() as cnn:
        cnn.execute(text(drop_database))
        cnn.execute(text(create_database))


def init_table():
    engine = create_engine(
        build_uri(SYNC_BACKEND, DB_NAME),
        echo=ECHO
    )
    with engine.connect() as cnn:
        Base.metadata.create_all(cnn)
        cnn.commit()

    with Session(engine).begin() as ss:
        default_user = User(
            usercount=USER_COUNT,
            password=User.gen_password(PASSWORD),
            type=UserType.ADMIN
        )
        ss.session.add(default_user)


def main():
    init_db()
    init_table()


if __name__ == "__main__":
    main()