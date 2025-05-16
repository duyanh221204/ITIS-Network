from sqlalchemy import Column, Integer, String, DateTime

from configs.database import Base


class InvalidatedToken(Base):
    __tablename__ = "invalidated_tokens"

    id = Column(Integer, primary_key=True, index=True)
    jwt_id = Column(String(255), index=True, nullable=False)
    expired_at = Column(DateTime, nullable=False)
