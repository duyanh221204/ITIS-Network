from pydantic import BaseModel


class LikeSchema(BaseModel):
    id: int
    liker_id: int
    liker_name: str
    liker_avatar: str | None = None
    post_id: int

    model_config = {
        "from_attributes": True
    }
