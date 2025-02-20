from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PasswordUpdateSchema(BaseModel):
    current_password: str
    new_password: str
