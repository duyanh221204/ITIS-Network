from fastapi import Depends
from sqlalchemy.orm import Session, selectinload

from models import Message
from schemas.chat import MessageCreateSchema
from utils.configs.database import get_db


def get_message_repository(db=Depends(get_db)):
    try:
        yield MessageRepository(db)
    finally:
        pass


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, conversation_id: int) -> list[type[Message]]:
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).options(
            selectinload(Message.sender)
        ).order_by(
            Message.created_at
        ).all()

    def create(self, conversation_id: int, sender_id: int, data: MessageCreateSchema) -> Message:
        msg = Message(
            content=data.content,
            sender_id=sender_id,
            conversation_id=conversation_id
        )

        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def mark_as_read(self, conversation_id: int, user_id: int) -> None:
        self.db.query(Message).filter(
            Message.conversation_id == conversation_id,
            Message.sender_id != user_id,
            Message.is_read == False
        ).update(
            {Message.is_read: True},
            synchronize_session=False
        )
        self.db.commit()
