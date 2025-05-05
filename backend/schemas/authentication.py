from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OTPRequestSchema(BaseModel):
    email: str


class PasswordResetSchema(OTPRequestSchema):
    new_password: str
