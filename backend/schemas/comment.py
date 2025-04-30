from pydantic import BaseModel


class CommentBaseSchema(BaseModel):
    content: str
    post_id: int


class CommentInfoSchema(CommentBaseSchema):
    id: int
    author_id: int
    author_name: str
    author_avatar: str | None = None

    model_config = {
        "from_attribute": True
    }
