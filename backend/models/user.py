from configs.database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    followers_number = Column(Integer, default=0, nullable=False)
    following_number = Column(Integer, default=0, nullable=False)
