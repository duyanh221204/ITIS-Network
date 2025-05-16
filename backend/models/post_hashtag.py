from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from configs.database import Base


class PostHashtag(Base):
    __tablename__ = "posts_hashtags"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), index=True, nullable=False)
    hashtag_id = Column(Integer, ForeignKey("hashtags.id", ondelete="CASCADE"), index=True, nullable=False)

    post = relationship("Post", back_populates="hashtags")
    hashtag = relationship("Hashtag", back_populates="posts")
