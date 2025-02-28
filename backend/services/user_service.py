from configs.authentication import hash_password, verify_password

from models.user import User
from models.follow import Follow

from schemas.user import UserRegisterSchema, UserProfileSchema
from schemas.base_response import BaseResponse
from schemas.authentication import PasswordUpdateSchema

from exceptions import raise_error

from sqlalchemy.orm import Session
from sqlalchemy.sql import func


def get_user_service():
    try:
        yield UserService()
    finally:
        pass


class UserService:
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

    def get_info(self, db: Session, user: dict) -> BaseResponse:
        user_db = db.query(User).filter(User.id == user["id"]).first()

        followers_number = db.query(func.count(Follow.followed_id)).filter(Follow.followed_id == user["id"]).scalar()
        followings_number = db.query(func.count(Follow.follower_id)).filter(Follow.follower_id == user["id"]).scalar()

        user_info = UserProfileSchema(
            username=user_db.username,
            email=user_db.email,
            followers_number=followers_number,
            followings_number=followings_number
        )
        return BaseResponse(message="Get user's info successfully", data=user_info)

    def update_password(self, data: PasswordUpdateSchema, db: Session, user: dict) -> BaseResponse:
        user_db = db.query(User).filter(User.id == user["id"]).first()
        if not verify_password(data.current_password, user_db.hashed_password):
            return raise_error(1005)

        user_db.hashed_password = hash_password(data.new_password)
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return BaseResponse(message="Password updated")
