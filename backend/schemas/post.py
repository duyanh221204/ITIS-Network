from pydantic import BaseModel


class PostCreate(BaseModel):
    content: str | None = None
    image: str | None = None
