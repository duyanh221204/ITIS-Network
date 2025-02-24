from configs.authentication import hash_password, verify_password

from models.user import User

from schemas.user import UserRegisterSchema
from schemas.base_response import BaseResponse
from schemas.authentication import PasswordUpdateSchema

from exceptions import raise_error

from sqlalchemy.orm import Session


def get_user_services():
    try:
        yield UserServices()
    finally:
        pass


class UserServices:
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

    def update_password(self, data: PasswordUpdateSchema, db: Session, user: dict) -> BaseResponse:
        user_db = db.query(User).filter(User.id == user["id"]).first()
        if not verify_password(data.current_password, user_db.hashed_password):
            return raise_error(1004)
        user_db.hashed_password = hash_password(data.new_password)
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return BaseResponse(message="Password updated")
