from datetime import datetime

from pydantic import BaseModel

from schemas.comment import CommentInfoSchema
from schemas.like import LikeSchema


class PostBaseSchema(BaseModel):
    content: str | None = None
    image: str | None = None


class PostInfoSchema(PostBaseSchema):
    id: int
    author_id: int
    author_name: str
    author_avatar: str | None = None
    created_at: datetime
    likes: list[LikeSchema]
    comments: list[CommentInfoSchema]

    model_config = {
        "from_attributes": True
    }
