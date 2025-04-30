from sqlalchemy import Column, Integer, String, Boolean, DATETIME, ForeignKey
from sqlalchemy.sql import func

from utils.configs.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000), nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DATETIME, server_default=func.now(), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
