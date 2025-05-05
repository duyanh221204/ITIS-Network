from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from utils.configs.database import Base


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    liker_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), index=True, nullable=False)

    liker = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
