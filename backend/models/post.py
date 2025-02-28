from configs.database import Base

from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000))
    image = Column(String(255))
    created_at = Column(DATETIME, server_default=func.now(), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)

    author = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post")
    comments = relationship("Comment", back_populates="post")

    __table_args__ = (CheckConstraint("content IS NOT NULL OR image IS NOT NULL"), )
