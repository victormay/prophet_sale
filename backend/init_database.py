import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import text, create_engine

load_dotenv()

from db.models import *
from db.engine import build_uri, SYNC_BACKEND, DB_NAME, ECHO


def init_db():
    engine = create_engine(
        build_uri(SYNC_BACKEND),
        echo=ECHO
    )
    drop_database = f"DROP DATABASE IF EXISTS {DB_NAME};"
    create_database = f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci;"
    
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
        admin_user = User(
            usercount="admin",
            password=User.gen_password("pdsf123456"),
            type=UserType.ADMIN,
            img = "admin.png"
            
        )
        normal_user = User(
            usercount="user",
            password=User.gen_password("123456"),
            type=UserType.USER,
            img="normal.png"
        )
        ss.session.add_all([admin_user, normal_user])


def main():
    init_db()   
    init_table()


if __name__ == "__main__":
    main()