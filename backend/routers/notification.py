from fastapi import APIRouter, Depends

from services.notification_service import get_notification_service
from utils.configs.authentication import get_current_user
from utils.configs.database import get_db
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
        return noti_service.mark_as_read(db, user["id"], noti_id)
    except Exception:
        return raise_error(3002)
