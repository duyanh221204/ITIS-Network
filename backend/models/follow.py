from utils.configs.database import Base
from sqlalchemy import Column, Integer, ForeignKey


class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    followed_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
