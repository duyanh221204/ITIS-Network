from schemas.post import PostBaseSchema
from services.post_service import get_post_service
from utils.configs.database import get_db
from utils.configs.authentication import get_current_user
from utils.exceptions import raise_error
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/api/post",
    tags=["Post"]
)


@router.post("/create")
def create_post(
        data: PostBaseSchema,
        db=Depends(get_db),
        user=Depends(get_current_user),
        post_service=Depends(get_post_service)
):
    try:
        return post_service.create_post(data, db, user["id"])
    except Exception:
        return raise_error(2002)


@router.put("/update/{post_id}")
def update_post_by_id(
        data: PostBaseSchema,
        post_id: int,
        db=Depends(get_db),
        _=Depends(get_current_user),
        post_service=Depends(get_post_service),
):
    try:
        return post_service.update_post_by_id(data, db, post_id)
    except Exception:
        return raise_error(2003)


@router.delete("/delete/{post_id}")
def delete_post_by_id(
        post_id: int,
        db=Depends(get_db),
        _=Depends(get_current_user),
        post_service=Depends(get_post_service),
):
    try:
        return post_service.delete_post_by_id(db, post_id)
    except Exception:
        return raise_error(2004)
