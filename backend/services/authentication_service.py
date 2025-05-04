import os
from datetime import timedelta

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models import User
from schemas.authentication import TokenSchema
from schemas.base_response import BaseResponse
from schemas.user import UserRegisterSchema
from utils.configs.authentication import hash_password, verify_password, create_access_token
from utils.exceptions import raise_error

load_dotenv()

ACCESS_TOKEN_EXPIRED_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRED_MINUTES")


def get_auth_service():
    try:
        yield AuthenticationService()
    finally:
        pass


class AuthenticationService:
    def register(self, data: UserRegisterSchema, db: Session) -> BaseResponse:
        if db.query(db.query(User).filter(User.username == data.username).exists()).scalar():
            return raise_error(1001)

        if db.query(db.query(User).filter(User.email == data.email).exists()).scalar():
            return raise_error(1002)

        new_user = User(
            username=data.username,
            email=data.email,
            avatar=data.avatar,
            introduction=data.introduction,
            hashed_password=hash_password(data.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return BaseResponse(message="Register successfully")

    def authenticate_user(self, data: OAuth2PasswordRequestForm, db: Session) -> TokenSchema | BaseResponse:
        user_db = db.query(User).filter(User.username == data.username).first()
        if user_db is None or not verify_password(data.password, user_db.hashed_password):
            return raise_error(1004)

        access_token = create_access_token(
            data={"sub": user_db.username, "id": user_db.id},
            expired_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRED_MINUTES))
        )
        return TokenSchema(access_token=access_token)
