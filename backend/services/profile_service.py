from sqlalchemy.orm import Session

from models import User, Follow
from schemas.base_response import BaseResponse
from schemas.user import UserMiniSchema, UserProfileSchema, UserInfoUpdateSchema
from utils.exceptions import raise_error


def get_profile_service():
    try:
        yield ProfileService()
    finally:
        pass


class ProfileService:
    def get_info(self, db: Session, user_id: int) -> BaseResponse:
        user_db = db.query(User).filter(User.id == user_id).first()

        followers_list = db.query(User).join(
            Follow,
            Follow.follower_id == User.id
        ).filter(Follow.followed_id == user_id).all()
        followers = [UserMiniSchema.model_validate(follower) for follower in followers_list]

        followings_list = db.query(User).join(
            Follow,
            Follow.followed_id == User.id
        ).filter(Follow.follower_id == user_id).all()
        followings = [UserMiniSchema.model_validate(following) for following in followings_list]

        user_info = UserProfileSchema(
            id=user_id,
            username=user_db.username,
            email=user_db.email,
            avatar=user_db.avatar,
            introduction=user_db.introduction,
            followers=followers,
            followings=followings
        )
        return BaseResponse(message="Get user's info successfully", data=user_info)

    def update_info(self, data: UserInfoUpdateSchema, db: Session, user_id: int) -> BaseResponse:
        existing_user = db.query(User).filter(
            User.username == data.username,
            User.id != user_id
        ).first()
        if existing_user is not None:
            return raise_error(1001)

        user_db = db.query(User).filter(User.id == user_id).first()
        _data = data.model_dump(exclude_unset=True).items()
        update_data = {key: value.strip() for key, value in _data if isinstance(value, str) and value.strip() != ""}

        if update_data:
            for key, value in update_data.items():
                setattr(user_db, key, value)

        db.commit()
        db.refresh(user_db)
        return BaseResponse(message="Update user's info successfully")
