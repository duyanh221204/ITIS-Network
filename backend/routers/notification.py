from fastapi import APIRouter, Depends, WebSocket, Query, status
from jose import jwt

from services.notification_service import get_notification_service
from utils.configs.authentication import get_current_user, SECRET_KEY, ALGORITHM
from utils.configs.database import get_db, SessionLocal
from utils.configs.websocket import websocket_manager
from utils.exceptions import raise_error

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notification"]
)


@router.get("/all")
def get_all_notifications(
        db=Depends(get_db),
        user=Depends(get_current_user),
        noti_service=Depends(get_notification_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return noti_service.get_all_notifications(db, user["id"])
    except Exception:
        return raise_error(3000)


@router.put("/{noti_id}")
def mark_as_read(
        noti_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        noti_service=Depends(get_notification_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return noti_service.mark_as_read(db, user["id"], noti_id)
    except Exception:
        return raise_error(3002)


@router.websocket("/ws")
async def notifications_websocket(
        websocket: WebSocket,
        token: str = Query(...),
        noti_service=Depends(get_notification_service)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if user_id is None or username is None:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket_manager.connect(user_id, websocket)
    db = SessionLocal()

    try:
        response = noti_service.get_unread_notifications(db, user_id)
        if response.status == "ok":
            await websocket.send_json(
                {
                    "type": "notifications",
                    "data": response.data
                }
            )
    finally:
        db.close()

    try:
        while True:
            await websocket.receive_text()
    except Exception:
        await websocket_manager.disconnect(user_id, websocket)
