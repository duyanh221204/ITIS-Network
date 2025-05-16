import random
from datetime import timedelta, datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from repositories.invalidated_token_repository import InvalidatedTokenRepository, get_invalidated_token_repository
from repositories.user_repository import get_user_repository, UserRepository
from schemas.authentication import TokenSchema, OTPRequestSchema, PasswordResetSchema
from schemas.base_response import BaseResponse
from schemas.user import UserRegisterSchema
from configs.authentication import verify_password, create_access_token, verify_token, decode_token
from configs.mail import send_email
from utils.constants import Constant
from utils.exceptions import raise_error

ACCESS_TOKEN_EXPIRED_MINUTES = Constant.ACCESS_TOKEN_EXPIRED_MINUTES


def get_auth_service(
        user_repository=Depends(get_user_repository),
        invalidated_token_repository=Depends(get_invalidated_token_repository)
):
    try:
        yield AuthenticationService(user_repository, invalidated_token_repository)
    finally:
        pass


class AuthenticationService:
    def __init__(self, user_repository: UserRepository, invalidated_token_repository: InvalidatedTokenRepository):
        self.user_repository = user_repository
        self.invalidated_token_repository = invalidated_token_repository

    def register(self, data: UserRegisterSchema) -> BaseResponse:
        user_db = self.user_repository.get_by_username(data.username)
        if user_db is not None:
            return raise_error(1001)

        user_db = self.user_repository.get_by_email(data.email)
        if user_db is not None:
            return raise_error(1002)

        self.user_repository.create(data)
        return BaseResponse(message="Register successfully")

    def authenticate_user(self, data: OAuth2PasswordRequestForm) -> TokenSchema | BaseResponse:
        user_db = self.user_repository.get_by_username(data.username)
        if user_db is None or not verify_password(data.password, user_db.hashed_password):
            return raise_error(1004)

        access_token = create_access_token(
            data={"sub": str(user_db.id)},
            expired_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRED_MINUTES))
        )
        return TokenSchema(access_token=access_token)

    def reset_password(self, data: PasswordResetSchema) -> BaseResponse:
        user_db = self.user_repository.get_by_email(data.email)
        if user_db is None:
            return raise_error(1004)

        self.user_repository.update_password(user_db, data.new_password)
        return BaseResponse(message="Reset password successfully")
    
    def send_otp(self, data: OTPRequestSchema) -> BaseResponse:
        code = f"{random.randint(0, 999999):06d}"
        subject = "[ITIS Network] Verification code"
        body = f"Your verification code is: {code}"

        try:
            send_email(data.email, subject, body)
        except Exception as e:
            print ("Sending email error:\n" + str(e))
            return raise_error(5000)

        return BaseResponse(message="OTP sent successfully", data=code)

    def refresh_token(self, token: str) -> TokenSchema | BaseResponse:
        verified_token = verify_token(token, self.invalidated_token_repository)
        if verified_token is None:
            return raise_error(1005)

        decoded_token = decode_token(token)
        self.invalidated_token_repository.save(
            decoded_token.get("id"),
            datetime.fromtimestamp(decoded_token.get("exp"))
        )

        access_token = create_access_token(
            data={"sub": str(verified_token.id)},
            expired_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRED_MINUTES))
        )
        return TokenSchema(access_token=access_token)

    def logout(self, token: str) -> BaseResponse:
        verified_token = verify_token(token, self.invalidated_token_repository)
        if verified_token is None:
            return raise_error(1005)

        decoded_token = decode_token(token)
        self.invalidated_token_repository.save(
            decoded_token.get("id"),
            datetime.fromtimestamp(decoded_token.get("exp"))
        )

        return BaseResponse(message="Logout successfully")
