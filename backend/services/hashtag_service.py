from fastapi import Depends

from repositories.hashtag_repository import get_hashtag_repository, HashtagRepository
from schemas.base_response import BaseResponse
from schemas.hashtag import HashTagCreateSchema, HashTagSchema


def get_hashtag_service(hashtag_repository=Depends(get_hashtag_repository)):
    try:
        yield HashtagService(hashtag_repository)
    finally:
        pass
    
    
class HashtagService:
    def __init__(self, hashtag_repository: HashtagRepository):
        self.hashtag_repository = hashtag_repository

    def get_or_create_hashtag(self, data: HashTagCreateSchema) -> BaseResponse:
        hashtag = data.name.strip().replace(" ", "")
        hashtag_db = self.hashtag_repository.get_by_name(hashtag)

        if hashtag_db is None:
            hashtag_db = self.hashtag_repository.create(data)

        return BaseResponse(data=HashTagSchema.model_validate(hashtag_db))

    def get_all_hashtags(self) -> BaseResponse:
        hashtags = self.hashtag_repository.get_all()
        data = [HashTagSchema.model_validate(hashtag) for hashtag in hashtags]
        return BaseResponse(message="Retrieving hashtags successfully", data=data)
