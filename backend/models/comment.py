from configs.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000))
    author_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), index=True, nullable=False)

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
