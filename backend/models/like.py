from configs.database import Base

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    liker_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), index=True, nullable=False)

    liker = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
