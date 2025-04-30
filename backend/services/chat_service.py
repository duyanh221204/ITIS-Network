from sqlalchemy.orm import Session

from models import User
from models.conversation import Conversation
from models.message import Message
from schemas.base_response import BaseResponse
from schemas.chat import ConversationSchema, MessageSchema, MessageCreateSchema
from schemas.user import UserMiniSchema
from utils.exceptions import raise_error


def get_chat_service():
    try:
        yield ChatService()
    finally:
        pass


class ChatService:
    def get_or_create_conversation(self, db: Session, user_id: int, other_user_id: int) -> BaseResponse:
        user1_id, user2_id = sorted([user_id, other_user_id])
        conversation = db.query(Conversation).filter(
            Conversation.user1_id == user1_id,
            Conversation.user2_id == user2_id
        ).first()

        if conversation is None:
            conversation = Conversation(user1_id=user1_id, user2_id=user2_id)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        response = ConversationSchema(
            id=conversation.id,
            participants=[
                UserMiniSchema.model_validate(
                    db.query(User).filter(
                        User.id.in_([conversation.user1_id, conversation.user2_id]),
                        User.id != user_id
                    ).first()
                )
            ],
            created_at=conversation.created_at
        )
        return BaseResponse(data=response)

    def get_all_conversations(self, db: Session, user_id: int) -> BaseResponse:
        conversations = db.query(Conversation).filter(
            (Conversation.user1_id == user_id) | (Conversation.user2_id == user_id)
        ).order_by(Conversation.created_at.desc()).all()

        data = []
        for cnv in conversations:
            other_user_id = cnv.user2_id if cnv.user1_id == user_id else cnv.user1_id
            other_user = db.query(User).filter(User.id == other_user_id).first()
            data.append(ConversationSchema(
                id=cnv.id,
                participants=[UserMiniSchema.model_validate(other_user)],
                created_at=cnv.created_at
            ))

        return BaseResponse(message="Conversations retrieved", data=data)

    def get_all_messages(self, db: Session, conversation_id: int, user_id: int) -> BaseResponse:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation is None or user_id not in {conversation.user1_id, conversation.user2_id}:
            return raise_error(4002)

        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()

        data = []
        for msg in messages:
            sender = db.query(User).filter(User.id == msg.sender_id).first()
            data.append(MessageSchema(
                id=msg.id,
                content=msg.content,
                is_read=msg.is_read,
                created_at=msg.created_at,
                sender=UserMiniSchema.model_validate(sender)
            ))

        return BaseResponse(message="Messages retrieved", data=data)

    def send_message(self, db: Session, conversation_id: int, user_id: int, data: MessageCreateSchema) -> BaseResponse:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation is None or user_id not in {conversation.user1_id, conversation.user2_id}:
            return raise_error(4002)

        msg = Message(
            content=data.content,
            sender_id=user_id,
            conversation_id=conversation_id
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return BaseResponse(message="Send message successfully", data=MessageSchema.model_validate(msg))

    def mark_as_read(self, db: Session, conversation_id: int, user_id: int) -> BaseResponse:
        db.query(Message).filter(
            Message.conversation_id == conversation_id,
            Message.sender_id != user_id,
            Message.is_read == False
        ).update({Message.is_read: True}, synchronize_session=False)
        db.commit()
        return BaseResponse(message="Conversation marked as read")
