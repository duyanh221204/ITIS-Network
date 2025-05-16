from pydantic import BaseModel


class HashtagSchema(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }
