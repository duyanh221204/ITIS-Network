from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr


class UserRegisterSchema(UserBaseSchema):
    avatar: str | None = None
    introduction: str | None = None
    password: str


class UserMiniSchema(BaseModel):
    id: int
    username: str
    avatar: str | None = None

    model_config = {
        "from_attributes": True
    }


class UserProfileSchema(UserBaseSchema):
    id: int
    avatar: str | None = None
    introduction: str | None = None
    followers: list[UserMiniSchema]
    followings: list[UserMiniSchema]


class UserInfoUpdateSchema(BaseModel):
    username: str | None = None
    avatar: str | None = None
    introduction: str | None = None


class UserPasswordUpdateSchema(BaseModel):
    current_password: str
    new_password: str
