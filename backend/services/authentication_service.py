import os
import random
from datetime import timedelta

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models import User
from schemas.authentication import TokenSchema, OTPRequestSchema, PasswordResetSchema
from schemas.base_response import BaseResponse
from schemas.user import UserRegisterSchema
from utils.configs.authentication import hash_password, verify_password, create_access_token
from utils.configs.mail import send_email
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
        user_db = db.query(User).filter(
            (User.username == data.username) | (User.email == data.email)
        ).first()

        if user_db is not None:
            return raise_error(1001) if user_db.username == data.username else raise_error(1002)

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
            data={"sub": str(user_db.id)},
            expired_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRED_MINUTES))
        )
        return TokenSchema(access_token=access_token)

    def reset_password(self, data: PasswordResetSchema, db: Session) -> BaseResponse:
        user_db = db.query(User).filter(User.email == data.email).first()
        if user_db is None:
            return raise_error(1004)

        user_db.hashed_password = hash_password(data.new_password)
        db.commit()
        db.refresh(user_db)
        return BaseResponse(message="Reset password successfully")
    
    def send_otp(self, data: OTPRequestSchema) -> BaseResponse:
        code = f"{random.randint(0, 999999):06d}"
        subject = "[ITIS Network] Verification code"
        body = f"Your verification code is: {code}"

        try:
            send_email(data.email, subject, body)
        except Exception:
            return raise_error(5000)

        return BaseResponse(message="OTP sent successfully", data=code)
