from fastapi import Depends

from repositories.user_repository import get_user_repository, UserRepository
from schemas.base_response import BaseResponse
from schemas.user import UserPasswordUpdateSchema, UserMiniSchema
from services.notification_service import get_notification_service, NotificationService
from utils.configs.authentication import verify_password
from utils.exceptions import raise_error


def get_user_service(
        user_repository=Depends(get_user_repository),
        notification_service=Depends(get_notification_service)
):
    try:
        yield UserService(user_repository, notification_service)
    finally:
        pass


class UserService:
    def __init__(self, user_repository: UserRepository, notification_service: NotificationService):
        self.user_repository = user_repository
        self.notification_service = notification_service

    def update_password(self, data: UserPasswordUpdateSchema, user_id: int) -> BaseResponse:
        user_db = self.user_repository.get_by_id(user_id)
        if not verify_password(data.current_password, user_db.hashed_password):
            return raise_error(1006)

        self.user_repository.update_password(user_db, data.new_password)
        return BaseResponse(message="Password updated")

    def follow_user(self, follower_id: int, followed_id: int) -> BaseResponse:
        self.user_repository.follow(follower_id, followed_id)
        return BaseResponse(message="Successfully follow user")

    def unfollow_user(self, follower_id: int, followed_id: int) -> BaseResponse:
        self.user_repository.unfollow(follower_id, followed_id)
        return BaseResponse(message="Successfully unfollow user")

    def get_not_followed_users(self, user_id: int) -> BaseResponse:
        users = self.user_repository.get_not_following(user_id)
        data = [UserMiniSchema.model_validate(user) for user in users]
        return BaseResponse(message="Users retrieved successfully", data=data)
