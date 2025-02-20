from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str
    email: str


class UserRegisterSchema(UserBaseSchema):
    password: str


class UserProfileSchema(UserBaseSchema):
    followers_number: int
    following_number: int
