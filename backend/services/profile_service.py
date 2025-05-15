from fastapi import Depends

from repositories.user_repository import get_user_repository, UserRepository
from schemas.base_response import BaseResponse
from schemas.user import UserMiniSchema, UserProfileSchema, UserInfoUpdateSchema
from utils.exceptions import raise_error


def get_profile_service(user_repository=Depends(get_user_repository)):
    try:
        yield ProfileService(user_repository)
    finally:
        pass


class ProfileService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_info(self, user_id: int) -> BaseResponse:
        user_db = self.user_repository.get_by_id(user_id)

        followers_list = self.user_repository.get_followers(user_id)
        followers = [UserMiniSchema.model_validate(follower) for follower in followers_list]

        followings_list = self.user_repository.get_followings(user_id)
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

    def update_info(self, data: UserInfoUpdateSchema, user_id: int) -> BaseResponse:
        existing_user = self.user_repository.get_by_username_and_id(data.username, user_id)
        if existing_user is not None:
            return raise_error(1001)

        user_db = self.user_repository.get_by_id(user_id)
        self.user_repository.update_info(user_db, data)
        return BaseResponse(message="Update user's info successfully")
