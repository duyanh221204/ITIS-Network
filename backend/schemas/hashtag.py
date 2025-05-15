from pydantic import BaseModel


class HashTagCreateSchema(BaseModel):
    name: str


class HashTagSchema(HashTagCreateSchema):
    id: int

    model_config = {
        "from_attributes": True
    }
