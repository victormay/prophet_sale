from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from app.config import Config


engine = create_async_engine(Config.SQLALCHEMY_DATABASE_URI,pool_pre_ping=True,echo=False,future=True)
sm = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)
Base = declarative_base()