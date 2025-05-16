from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from configs.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    avatar = Column(String(255))
    introduction = Column(String(255))

    posts = relationship("Post", back_populates="author", passive_deletes=True)
    likes = relationship("Like", back_populates="liker", passive_deletes=True)
    comments = relationship("Comment", back_populates="author", passive_deletes=True)
    followers = relationship("Follow", foreign_keys="[Follow.followed_id]", back_populates="followed", passive_deletes=True)
    followings = relationship("Follow", foreign_keys="[Follow.follower_id]", back_populates="follower", passive_deletes=True)
    conversations_user1 = relationship("Conversation", foreign_keys="[Conversation.user1_id]", back_populates="user1")
    conversations_user2 = relationship("Conversation", foreign_keys="[Conversation.user2_id]", back_populates="user2")
    messages = relationship("Message", back_populates="sender")
    notifications_sent = relationship("Notification", foreign_keys="[Notification.actor_id]", back_populates="actor")
    notifications_received = relationship("Notification", foreign_keys="[Notification.receiver_id]", back_populates="receiver")
