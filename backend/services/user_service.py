from models.notification import Notification, NotificationType
from models.user import User
from models.follow import Follow
from schemas.user import UserPasswordUpdateSchema, UserMiniSchema
from schemas.base_response import BaseResponse
from utils.configs.authentication import hash_password, verify_password
from utils.exceptions import raise_error
from sqlalchemy.orm import Session


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
        followed = db.query(Follow.followed_id).filter(Follow.follower_id == user_id).all()
        exclude_ids = {result[0] for result in followed} | {user_id}
        users = db.query(User).filter(User.id.notin_(exclude_ids)).all()

        data = [UserMiniSchema.model_validate(user) for user in users]
        return BaseResponse(message="Users retrieved successfully", data=data)
