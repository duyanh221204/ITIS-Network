from sqlalchemy.orm import Session

from models import User
from models.notification import Notification
from schemas.base_response import BaseResponse
from schemas.notification import NotificationSchema
from utils.exceptions import raise_error


def get_notification_service():
    try:
        yield NotificationService()
    finally:
        pass


class NotificationService:
    def get_all_notifications(self, db: Session, user_id: int) -> BaseResponse:
        notis = db.query(Notification).filter(Notification.receiver_id == user_id).order_by(
            Notification.created_at.desc()
        ).all()

        data = []
        for noti in notis:
            actor = db.query(User).filter(User.id == noti.actor_id).first() if noti.actor_id else None
            data.append(NotificationSchema(
                id=noti.id,
                actor=actor,
                type=noti.type,
                post_id=noti.post_id,
                is_read=noti.is_read,
                created_at=noti.created_at
            ))

        return BaseResponse(message="All notifications retrieved", data=data)

    def mark_as_read(self, db: Session, user_id: int, noti_id) -> BaseResponse:
        noti = db.query(Notification).filter(
            Notification.id == noti_id,
            Notification.receiver_id == user_id
        ).first()

        if noti is None:
            return raise_error(3001)

        noti.is_read = True
        db.commit()
        db.refresh(noti)
        return BaseResponse(message="Marked notification as read")
