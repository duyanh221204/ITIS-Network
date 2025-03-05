from configs.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    avatar = Column(String(255))
    introduction = Column(String(255))

    posts = relationship("Post", back_populates="author")
    followers = relationship("Follow", foreign_keys="Follow.followed_id", back_populates="followed")
    followings = relationship("Follow", foreign_keys="Follow.follower_id", back_populates="follower")
    likes = relationship("Like", back_populates="liker")
    comments = relationship("Comment", back_populates="author")
