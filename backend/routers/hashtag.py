from fastapi import APIRouter, Depends

from schemas.authentication import TokenDataSchema
from services.hashtag_service import HashtagService, get_hashtag_service
from utils.configs.authentication import get_current_user
from utils.exceptions import raise_error

router = APIRouter(
    prefix="/api/hashtags",
    tags=["Hashtag"]
)


@router.get("/all")
async def get_all_hashtags(
        user: TokenDataSchema = Depends(get_current_user),
        hashtag_service: HashtagService = Depends(get_hashtag_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return hashtag_service.get_all_hashtags()
    except Exception as e:
        print ("Retrieving all hashtags error:\n" + str(e))
        return raise_error(6001)
