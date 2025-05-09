from fastapi import APIRouter, Depends, WebSocket, Query, status
from fastapi.encoders import jsonable_encoder

from services.notification_service import get_notification_service
from utils.configs.authentication import get_current_user
from utils.configs.database import get_db, SessionLocal
from utils.configs.websocket import websocket_manager, can_connect
from utils.exceptions import raise_error

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notification"]
)


@router.get("/all")
async def get_all_notifications(
        db=Depends(get_db),
        user=Depends(get_current_user),
        noti_service=Depends(get_notification_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return noti_service.get_all_notifications(db, user.get("id"))
    except Exception as e:
        print ("Getting all notifications error:\n", str(e))
        return raise_error(3000)


@router.put("/{noti_id}")
async def mark_as_read(
        noti_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        noti_service=Depends(get_notification_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return noti_service.mark_as_read(db, user.get("id"), noti_id)
    except Exception as e:
        print ("Marking notification as read error:\n", str(e))
        return raise_error(3002)


@router.websocket("/ws")
async def notifications_websocket(
        websocket: WebSocket,
        token: str = Query(...),
        noti_service=Depends(get_notification_service)
):
    await websocket.accept()

    user_id = can_connect(token)
    if user_id is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    websocket_manager.connect(user_id, websocket)
    db = SessionLocal()

    try:
        response = noti_service.get_unread_notifications(db, user_id)
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
