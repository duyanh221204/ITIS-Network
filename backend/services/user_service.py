from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User, Follow, Notification
from models.notification import NotificationType
from schemas.base_response import BaseResponse
from schemas.user import UserPasswordUpdateSchema, UserMiniSchema
from utils.configs.authentication import verify_password, hash_password
from utils.exceptions import raise_error


def get_user_service():
    try:
        yield UserService()
    finally:
        pass


class UserService:
    def update_password(self, data: UserPasswordUpdateSchema, db: Session, user_id: int) -> BaseResponse:
        user_db = db.query(User).filter(User.id == user_id).first()
        if not verify_password(data.current_password, user_db.hashed_password):
            return raise_error(1006)

        user_db.hashed_password = hash_password(data.new_password)
        db.commit()
        db.refresh(user_db)
        return BaseResponse(message="Password updated")

    def follow_user(self, db: Session, follower_id: int, followed_id: int) -> BaseResponse:
        new_follow = Follow(
            follower_id=follower_id,
            followed_id=followed_id
        )
        db.add(new_follow)
        
        db.add(Notification(
            type=NotificationType.FOLLOW,
            actor_id=follower_id,
            receiver_id=followed_id
        ))

        db.commit()
        db.refresh(new_follow)
        return BaseResponse(message="Successfully follow user")

    def unfollow_user(self, db: Session, follower_id: int, followed_id: int) -> BaseResponse:
        follow_db = db.query(Follow).filter(
            follower_id == follower_id,
            followed_id == followed_id
        ).first()

        db.delete(follow_db)
        db.commit()
        return BaseResponse(message="Successfully unfollow user")

    def get_not_followed_users(self, db: Session, user_id: int) -> BaseResponse:
        followings = select(Follow.followed_id).where(Follow.follower_id == user_id)
        users = db.query(User).filter(
            User.id.notin_(followings),
            User.id != user_id
        ).all()

        data = [UserMiniSchema.model_validate(user) for user in users]
        return BaseResponse(message="Users retrieved successfully", data=data)
