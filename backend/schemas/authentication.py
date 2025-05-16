from pydantic import BaseModel, EmailStr


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenDataSchema(BaseModel):
    id: int


class OTPRequestSchema(BaseModel):
    email: EmailStr


class PasswordResetSchema(OTPRequestSchema):
    new_password: str
