from sqlalchemy import Integer, Column, ForeignKey, DATETIME
from sqlalchemy.sql import func

from utils.configs.database import Base


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user2_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DATETIME, server_default=func.now(), nullable=False)
