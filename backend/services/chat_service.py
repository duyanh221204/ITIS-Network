from fastapi import Depends

from repositories.conversation_repository import get_conversation_repository, ConversationRepository
from repositories.message_repository import get_message_repository, MessageRepository
from schemas.base_response import BaseResponse
from schemas.chat import ConversationSchema, MessageSchema, MessageCreateSchema, UnreadConversationsSchema
from schemas.user import UserMiniSchema
from utils.exceptions import raise_error


def get_chat_service(
        conversation_repository=Depends(get_conversation_repository),
        message_repository=Depends(get_message_repository)
):
    try:
        yield ChatService(conversation_repository, message_repository)
    finally:
        pass


class ChatService:
    def __init__(self, conversation_repository: ConversationRepository, message_repository: MessageRepository):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository

    def get_or_create_conversation(self, user_id: int, other_user_id: int) -> BaseResponse:
        user1_id, user2_id = sorted([user_id, other_user_id])
        conversation = self.conversation_repository.get_by_user_id(user1_id, user2_id)

        if conversation is None:
            self.conversation_repository.create(user1_id, user2_id)

        response = ConversationSchema(
            id=conversation.id,
            participants=[
                UserMiniSchema.model_validate(
                    conversation.user1 if conversation.user1_id != user_id else conversation.user2
                )
            ],
            created_at=conversation.created_at
        )
        return BaseResponse(data=response)

    def get_all_conversations(self, user_id: int) -> BaseResponse:
        conversations = self.conversation_repository.get_all(user_id)

        data = []
        for cnv in conversations:
            other = cnv.user1 if cnv.user2_id == user_id else cnv.user2
            data.append(ConversationSchema(
                id=cnv.id,
                participants=[UserMiniSchema.model_validate(other)],
                created_at=cnv.created_at
            ))

        return BaseResponse(message="Conversations retrieved", data=data)

    def get_all_messages(self, conversation_id: int, user_id: int) -> BaseResponse:
        conversation = self.conversation_repository.get_by_id(conversation_id)
        if conversation is None or user_id not in {conversation.user1_id, conversation.user2_id}:
            return raise_error(4002)

        messages = self.message_repository.get_all(conversation_id)

        data = [
            MessageSchema(
                id=msg.id,
                content=msg.content,
                is_read=msg.is_read,
                created_at=msg.created_at,
                sender=UserMiniSchema.model_validate(msg.sender)
            )
            for msg in messages
        ]

        return BaseResponse(message="Messages retrieved", data=data)

    def send_message(self, conversation_id: int, user_id: int, data: MessageCreateSchema) -> BaseResponse:
        conversation = self.conversation_repository.get_by_id(conversation_id)
        if conversation is None or user_id not in {conversation.user1_id, conversation.user2_id}:
            return raise_error(4002)

        msg = self.message_repository.create(conversation_id, user_id, data)
        return BaseResponse(message="Send message successfully", data=MessageSchema.model_validate(msg))

    def mark_as_read(self, conversation_id: int, user_id: int) -> BaseResponse:
        self.message_repository.mark_as_read(conversation_id, user_id)
        return BaseResponse(message="Conversation marked as read")

    def unread_count(self, user_id: int) -> BaseResponse:
        ids = self.conversation_repository.get_unread(user_id)
        data = UnreadConversationsSchema(
            count=len(ids),
            ids=ids
        )
        return BaseResponse(message="Unread conversations retrieved successfully", data=data)
