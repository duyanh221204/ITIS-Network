from configs.authentication import hash_password

from models.user import User

from schemas.user import UserRegisterSchema
from schemas.base_response import BaseResponse

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
            hashed_password=hash_password(data.password),
            email=data.email
        )
        db.add(user_regis)
        db.commit()
        db.refresh(user_regis)
        return BaseResponse(message="Register successfully")
