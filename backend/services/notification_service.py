from sqlalchemy.orm import Session, selectinload

from models import Notification
from models.notification import NotificationType
from schemas.base_response import BaseResponse
from schemas.notification import NotificationSchema
from schemas.user import UserMiniSchema
from utils.exceptions import raise_error


def get_notification_service():
    try:
        yield NotificationService()
    finally:
        pass


class NotificationService:
    def notify(
            self, db: Session, actor_id: int, receiver_id: int, noti_type: NotificationType, post_id: int | None = None
    ) -> BaseResponse:
        noti = Notification(
            type=noti_type,
            actor_id=actor_id,
            receiver_id=receiver_id,
            post_id=post_id
        )
        db.add(noti)
        db.commit()
        db.refresh(noti)

        new_noti = db.query(Notification).options(
            selectinload(Notification.actor)
        ).filter(
            Notification.id == noti.id
        ).first()

        data = NotificationSchema.model_validate(new_noti)
        return BaseResponse(message="Notification created", data=data)

    def get_notifications(self, notis) -> BaseResponse:
        data = [
            NotificationSchema(
                id=noti.id,
                actor=UserMiniSchema.model_validate(noti.actor),
                type=noti.type,
                post_id=noti.post_id,
                is_read=noti.is_read,
                created_at=noti.created_at
            )
            for noti in notis
        ]
        return BaseResponse(message="All notifications retrieved", data=data)

    def get_all_notifications(self, db: Session, user_id: int) -> BaseResponse:
        notis = db.query(Notification).filter(
            Notification.receiver_id == user_id
        ).options(
            selectinload(Notification.actor)
        ).order_by(
            Notification.created_at.desc()
        ).all()

        return self.get_notifications(notis)

    def get_unread_notifications(self, db: Session, user_id: int) -> BaseResponse:
        unread_notis = db.query(Notification).filter(
            Notification.receiver_id == user_id,
            Notification.is_read == False
        ).options(
            selectinload(Notification.actor)
        ).order_by(
            Notification.created_at.desc()
        ).all()

        return self.get_notifications(unread_notis)

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
