from models.user import User
from models.follow import Follow
from schemas.user import UserProfileSchema, UserInfoUpdateSchema, UserMiniSchema
from schemas.base_response import BaseResponse
from utils.exceptions import raise_error
from sqlalchemy.orm import Session


def get_profile_service():
    try:
        yield ProfileService()
    finally:
        pass


class ProfileService:
    def get_info(self, db: Session, user_id: int) -> BaseResponse:
        user_db = db.query(User).filter(User.id == user_id).first()

        followers = db.query(Follow.follower_id).filter(Follow.followed_id == user_id).all()
        followers_id = [result[0] for result in followers]
        followers_users = db.query(User).filter(User.id.in_(followers_id)).all()
        followers_list = [UserMiniSchema.model_validate(user) for user in followers_users]

        followings = db.query(Follow.followed_id).filter(Follow.follower_id == user_id).all()
        followings_id = [result[0] for result in followings]
        followings_users = db.query(User).filter(User.id.in_(followings_id)).all()
        followings_list = [UserMiniSchema.model_validate(user) for user in followings_users]

        user_info = UserProfileSchema(
            id=user_id,
            username=user_db.username,
            email=user_db.email,
            avatar=user_db.avatar,
            introduction=user_db.introduction,
            followers=followers_list,
            followings=followings_list
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

        db.commit()
        db.refresh(user_db)
        return BaseResponse(message="Update user's info successfully")
