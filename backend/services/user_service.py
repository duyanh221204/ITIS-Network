from models.user import User
from models.follow import Follow
from schemas.user import UserProfileSchema, UserInfoUpdateSchema, UserPasswordUpdateSchema
from schemas.base_response import BaseResponse
from utils.configs.authentication import hash_password, verify_password
from utils.exceptions import raise_error
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


def get_user_service():
    try:
        yield UserService()
    finally:
        pass


class UserService:
    def get_info(self, db: Session, user_id: int) -> BaseResponse:
        user_db = db.query(User).filter(User.id == user_id).first()

        followers_number = db.query(func.count(Follow.followed_id)).filter(Follow.followed_id == user_id).scalar()
        followings_number = db.query(func.count(Follow.follower_id)).filter(Follow.follower_id == user_id).scalar()

        user_info = UserProfileSchema(
            id=user_id,
            username=user_db.username,
            email=user_db.email,
            followers_number=followers_number,
            followings_number=followings_number
        )
        return BaseResponse(message="Get user's info successfully", data=user_info)

    def update_info(self, data: UserInfoUpdateSchema, db: Session, user_id: int) -> BaseResponse:
        existing_user = db.query(User).filter(
            (User.username == data.username) | (User.email == data.email),
            User.id != user_id
        ).first()
        if existing_user is not None:
            if existing_user.username == data.username:
                return raise_error(1001)
            return raise_error(1002)

        user_db = db.query(User).filter(User.id == user_id).first()
        _data = data.model_dump(exclude_unset=True).items()
        update_data = {key: value.strip() for key, value in _data if isinstance(value, str) and value.strip() != ""}

        if update_data:
            for key, value in update_data.items():
                setattr(user_db, key, value)
        return BaseResponse(message="Update user's info successfully")

    def update_password(self, data: UserPasswordUpdateSchema, db: Session, user_id: int) -> BaseResponse:
        user_db = db.query(User).filter(User.id == user_id).first()
        if not verify_password(data.current_password, user_db.hashed_password):
            return raise_error(1006)

        user_db.hashed_password = hash_password(data.new_password)
        db.commit()
        db.refresh(user_db)
        return BaseResponse(message="Password updated")
