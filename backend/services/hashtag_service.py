from fastapi import Depends

from repositories.hashtag_repository import get_hashtag_repository, HashtagRepository
from schemas.base_response import BaseResponse
from schemas.hashtag import HashtagSchema


def get_hashtag_service(hashtag_repository=Depends(get_hashtag_repository)):
    try:
        yield HashtagService(hashtag_repository)
    finally:
        pass
    
    
class HashtagService:
    def __init__(self, hashtag_repository: HashtagRepository):
        self.hashtag_repository = hashtag_repository

    def get_all_hashtags(self) -> BaseResponse:
        hashtags = self.hashtag_repository.get_all()
        data = [HashtagSchema.model_validate(hashtag) for hashtag in hashtags]
        return BaseResponse(message="Retrieving hashtags successfully", data=data)
