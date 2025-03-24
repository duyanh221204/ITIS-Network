from models.user import User
from models.follow import Follow
from schemas.user import UserPasswordUpdateSchema
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

