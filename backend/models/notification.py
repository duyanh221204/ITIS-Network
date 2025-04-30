from utils.configs.database import Base
from sqlalchemy import Column, Integer, Boolean, DATETIME, ForeignKey, Enum
from sqlalchemy.sql import func
import enum


class NotificationType(str, enum.Enum):
    FOLLOW = "follow"
    LIKE = "like"
    COMMENT = "comment"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(NotificationType), nullable=False)
    created_at = Column(DATETIME, server_default=func.now(), nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    actor_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), index=True)
