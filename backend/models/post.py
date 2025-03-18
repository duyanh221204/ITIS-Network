from utils.configs.database import Base
from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey
from sqlalchemy.sql import func


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000))
    image = Column(String(255))
    created_at = Column(DATETIME, server_default=func.now(), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
