from pydantic import BaseModel
from datetime import datetime
from typing import List
from schemas.user import UserProfileSchema


class PostBaseSchema(BaseModel):
    content: str | None = None
    image: str | None = None


class PostInfoSchema(PostBaseSchema):
    created_at: datetime
    likes: List[UserProfileSchema]
