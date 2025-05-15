from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from utils.configs.database import Base


class Hashtag(Base):
    __tablename__ = "hashtags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    posts = relationship("PostHashtag", back_populates="hashtag")
