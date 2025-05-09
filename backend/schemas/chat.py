from datetime import datetime

from pydantic import BaseModel

from schemas.user import UserMiniSchema


class ConversationCreateSchema(BaseModel):
    user_id: int


class ConversationSchema(BaseModel):
    id: int
    participants: list[UserMiniSchema]
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }


class MessageCreateSchema(BaseModel):
    content: str


class MessageSchema(BaseModel):
    id: int
    sender: UserMiniSchema
    content: str
    is_read: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
    
    
class UnreadConversationsSchema(BaseModel):
    count: int
    ids: list[int]
