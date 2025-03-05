from configs.authentication import create_access_token, hash_password, verify_password
from models.user import User
from schemas.authentication import TokenSchema
from schemas.base_response import BaseResponse
from schemas.user import UserRegisterSchema
from exceptions import raise_error
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_EXPIRED_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRED_MINUTES")


def get_auth_service():
    try:
        yield AuthenticationService()
    finally:
        pass


class AuthenticationService:
    def register(self, data: UserRegisterSchema, db: Session) -> BaseResponse:
        existing_user = db.query(User).filter(User.username == data.username).first()
        if existing_user is not None:
            return raise_error(1001)

        existing_user = db.query(User).filter(User.email == data.email).first()
        if existing_user is not None:
            return raise_error(1002)

        user_regis = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password)
        )
        db.add(user_regis)
        db.commit()
        db.refresh(user_regis)
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
