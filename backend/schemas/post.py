from datetime import datetime

from pydantic import BaseModel

from schemas.comment import CommentInfoSchema
from schemas.hashtag import HashtagSchema
from schemas.like import LikeSchema


class PostBaseSchema(BaseModel):
    content: str | None = None
    image: str | None = None
    
    
class PostCreateSchema(PostBaseSchema):
    hashtags: list[str] | None = None
    
    
class PostUpdateSchema(PostCreateSchema):
    ...


class PostInfoSchema(PostBaseSchema):
    id: int
    hashtags: list[HashtagSchema] | None = None
    author_id: int
    author_name: str
    author_avatar: str | None = None
    created_at: datetime
    likes: list[LikeSchema] | None = None
    comments: list[CommentInfoSchema] | None = None

    model_config = {
        "from_attributes": True
    }
