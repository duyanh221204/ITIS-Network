from sqlalchemy import Integer, Column, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from utils.configs.database import Base


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user2_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user1 = relationship("User", foreign_keys="[Conversation.user1_id]", back_populates="conversations_user1")
    user2 = relationship("User", foreign_keys="[Conversation.user2_id]", back_populates="conversations_user2")
    messages = relationship("Message", back_populates="conversation")
