from schemas.user import UserPasswordUpdateSchema
from services.user_service import get_user_service
from utils.configs.authentication import get_current_user
from utils.configs.database import get_db
from utils.exceptions import raise_error
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/api/user",
    tags=["User"]
)


@router.put("/update_password")
def update_password(
        data: UserPasswordUpdateSchema,
        db=Depends(get_db),
        user=Depends(get_current_user),
        user_service=Depends(get_user_service)
):
    try:
        return user_service.update_password(data, db, user["id"])
    except Exception:
        return raise_error(1007)


@router.post("/follow/{user_id}")
def follow_user(
        user_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        user_service=Depends(get_user_service)
):
    try:
        return user_service.follow_user(db, user["id"], user_id)
    except Exception:
        return raise_error(1010)


@router.delete("/unfollow/{user_id}")
def unfollow_user(
        user_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        user_service=Depends(get_user_service)
):
    try:
        return user_service.unfollow_user(db, user["id"], user_id)
    except Exception:
        return raise_error(1011)
