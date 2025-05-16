from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from utils.configs.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000))
    image = Column(String(255))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    
    hashtags = relationship("PostHashtag", back_populates="post", passive_deletes=True)
    author = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post", passive_deletes=True)
    comments = relationship("Comment", back_populates="post", passive_deletes=True)
    notifications = relationship("Notification", back_populates="post")
