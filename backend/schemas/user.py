from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str
    email: str


class UserRegisterSchema(UserBaseSchema):
    password: str


class UserProfileSchema(UserBaseSchema):
    avatar: str | None = None
    introduction: str | None = None
    followers_number: int
    followings_number: int


class UserInfoUpdateSchema(BaseModel):
    username: str | None = None
    email: str | None = None
    avatar: str | None = None
    introduction: str | None = None


class UserPasswordUpdateSchema(BaseModel):
    current_password: str
    new_password: str
