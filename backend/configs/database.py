from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.constants import Constant

USERNAME = Constant.MYSQL_USERNAME
PASSWORD = Constant.MYSQL_PASSWORD
HOST = Constant.MYSQL_HOST
PORT = Constant.MYSQL_PORT
DATABASE = Constant.MYSQL_DATABASE

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
