from fastapi import APIRouter, Depends, WebSocket, Query, status
from fastapi.encoders import jsonable_encoder

from schemas.authentication import TokenDataSchema
from services.notification_service import get_notification_service, NotificationService
from configs.authentication import get_current_user
from configs.database import SessionLocal
from configs.websocket import websocket_manager, can_connect
from utils.exceptions import raise_error

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notification"]
)


@router.get("/all")
async def get_all_notifications(
        user: TokenDataSchema = Depends(get_current_user),
        noti_service: NotificationService = Depends(get_notification_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return noti_service.get_all_notifications(user.id)
    except Exception as e:
        print ("Retrieving all notifications error:\n" + str(e))
        return raise_error(3000)


@router.put("/{noti_id}")
async def mark_as_read(
        noti_id: int,
        user: TokenDataSchema = Depends(get_current_user),
        noti_service: NotificationService = Depends(get_notification_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return noti_service.mark_as_read(user.id, noti_id)
    except Exception as e:
        print ("Marking notification as read error:\n" + str(e))
        return raise_error(3002)


@router.websocket("/ws")
async def notifications_websocket(
        websocket: WebSocket,
        _: str = Query(...),
        user: TokenDataSchema = Depends(can_connect),
        noti_service: NotificationService = Depends(get_notification_service)
):
    await websocket.accept()

    if user is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id = user.id
    websocket_manager.connect(user_id, websocket)
    db = SessionLocal()

    try:
        response = noti_service.get_unread_notifications(user_id)
        if response.status == "ok":
            await websocket.send_json(
                {
                    "type": "notifications",
                    "data": jsonable_encoder(response.data)
                }
            )
    finally:
        db.close()

    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        print ("Websocket exception:\n" + str(e))
    finally:
        websocket_manager.disconnect(user_id, websocket)
