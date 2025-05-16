from fastapi import Depends
from sqlalchemy import distinct, ColumnElement
from sqlalchemy.orm import Session, selectinload

from models import Conversation, Message
from utils.configs.database import get_db


def get_conversation_repository(db=Depends(get_db)):
    try:
        yield ConversationRepository(db)
    finally:
        pass


class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, conversation_id: int) -> Conversation | None:
        return self.db.query(Conversation).filter(Conversation.id == conversation_id).first()

    def get_by_user_id(self, user_id: int, other_user_id: int) -> Conversation | None:
        return self.db.query(Conversation).filter(
            Conversation.user1_id == user_id,
            Conversation.user2_id == other_user_id
        ).options(
            selectinload(Conversation.user1),
            selectinload(Conversation.user2)
        ).first()

    def create(self, user_id: int, other_user_id: int) -> None:
        conversation = Conversation(user1_id=user_id, user2_id=other_user_id)
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

    def get_all(self, user_id: int) -> list[type[Conversation]]:
        return self.db.query(Conversation).filter(
            (Conversation.user1_id == user_id) | (Conversation.user2_id == user_id)
        ).options(
            selectinload(Conversation.user1),
            selectinload(Conversation.user2)
        ).order_by(
            Conversation.created_at.desc()
        ).all()

    def get_unread(self, user_id: int) -> list[ColumnElement[int]]:
        return [
            result[0] for result in self.db.query(distinct(Message.conversation_id)).filter(
                Message.sender_id != user_id,
                Message.is_read == False
            ).all()
        ]
