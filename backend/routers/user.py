from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from models.notification import NotificationType
from schemas.authentication import TokenDataSchema
from schemas.user import UserPasswordUpdateSchema
from services.user_service import get_user_service, UserService
from configs.authentication import get_current_user
from configs.websocket import websocket_manager
from utils.exceptions import raise_error

router = APIRouter(
    prefix="/api/users",
    tags=["User"]
)


@router.put("/update-password")
async def update_password(
        data: UserPasswordUpdateSchema,
        user: TokenDataSchema = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return user_service.update_password(data, user.id)
    except Exception as e:
        print ("Updating password error:\n" + str(e))
        return raise_error(1007)


@router.post("/follow/{user_id}")
async def follow_user(
        user_id: int,
        user: TokenDataSchema = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    try:
        if user is None:
            return raise_error(1005)

        response = user_service.follow_user(user.id, user_id)
        if response.status == "ok":
            noti = user_service.notification_service.notify(user.id, user_id, NotificationType.FOLLOW)

            if noti.status == "ok":
                new_noti = noti.data
                payload: dict = {
                    "type": "new_notification",
                    "data": {
                        "id": new_noti.id,
                        "type": new_noti.type,
                        "is_read": new_noti.is_read,
                        "created_at": new_noti.created_at.isoformat(),
                        "actor_id": new_noti.actor.id,
                    }
                }

                await websocket_manager.broadcast(user_id, jsonable_encoder(payload))
        return response
    except Exception as e:
        print ("Follow error:\n" + str(e))
        return raise_error(1010)


@router.delete("/unfollow/{user_id}")
async def unfollow_user(
        user_id: int,
        user: TokenDataSchema = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return user_service.unfollow_user(user.id, user_id)
    except Exception as e:
        print ("Unfollow error:\n" + str(e))
        return raise_error(1011)


@router.get("")
async def get_not_followed_users(
        user: TokenDataSchema = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return user_service.get_not_followed_users(user.id)
    except Exception as e:
        print ("Retrieving users error:\n" + str(e))
        return raise_error(1012)
