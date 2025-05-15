import enum

from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, Enum, func
from sqlalchemy.orm import relationship

from utils.configs.database import Base


class NotificationType(str, enum.Enum):
    FOLLOW = "follow"
    LIKE = "like"
    COMMENT = "comment"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(NotificationType), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    actor_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), index=True)

    actor = relationship("User", foreign_keys="[Notification.actor_id]", back_populates="notifications_sent")
    receiver = relationship("User", foreign_keys="[Notification.receiver_id]", back_populates="notifications_received")
    post = relationship("Post", back_populates="notifications")
