from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from utils.configs.database import Base


class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    followed_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    follower = relationship("User", foreign_keys="[Follow.follower_id]", back_populates="followings")
    followed = relationship("User", foreign_keys="[Follow.followed_id]", back_populates="followers")
