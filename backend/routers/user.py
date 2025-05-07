from fastapi import APIRouter, Depends, BackgroundTasks

from models.notification import NotificationType
from schemas.user import UserPasswordUpdateSchema
from services.user_service import get_user_service
from utils.configs.authentication import get_current_user
from utils.configs.database import get_db
from utils.exceptions import raise_error

router = APIRouter(
    prefix="/api/users",
    tags=["User"]
)


@router.put("/update-password")
async def update_password(
        data: UserPasswordUpdateSchema,
        db=Depends(get_db),
        user=Depends(get_current_user),
        user_service=Depends(get_user_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return user_service.update_password(data, db, user["id"])
    except Exception:
        return raise_error(1007)


@router.post("/follow/{user_id}")
async def follow_user(
        user_id: int,
        background_tasks: BackgroundTasks,
        db=Depends(get_db),
        user=Depends(get_current_user),
        user_service=Depends(get_user_service)
):
    try:
        if user is None:
            return raise_error(1005)

        response = user_service.follow_user(db, user["id"], user_id)
        if response.status == "ok":
            background_tasks.add_task(
                user_service.notification_service.notify,
                db,
                user["id"],
                user_id,
                NotificationType.FOLLOW,
                None
            )
        return response
    except Exception:
        return raise_error(1010)


@router.delete("/unfollow/{user_id}")
async def unfollow_user(
        user_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        user_service=Depends(get_user_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return user_service.unfollow_user(db, user["id"], user_id)
    except Exception:
        return raise_error(1011)


@router.get("")
async def get_not_followed_users(
        db=Depends(get_db),
        user=Depends(get_current_user),
        user_service=Depends(get_user_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return user_service.get_not_followed_users(db, user["id"])
    except Exception:
        return raise_error(1012)
