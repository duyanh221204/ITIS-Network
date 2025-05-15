from fastapi import Depends
from sqlalchemy.orm import Session, selectinload

from models.notification import NotificationType, Notification
from utils.configs.database import get_db


def get_notification_repository(db=Depends(get_db)):
    try:
        yield NotificationRepository(db)
    finally:
        pass


class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
            self, actor_id: int, receiver_id: int, noti_type: NotificationType, post_id: int | None = None
    ) -> Notification:
        new_noti = Notification(
            type=noti_type,
            actor_id=actor_id,
            receiver_id=receiver_id,
            post_id=post_id
        )

        self.db.add(new_noti)
        self.db.commit()
        self.db.refresh(new_noti)
        return new_noti

    def get_by_id(self, notification_id: int) -> Notification | None:
        return self.db.query(Notification).options(
            selectinload(Notification.actor)
        ).filter(
            Notification.id == notification_id
        ).first()

    def get_by_id_and_user_id(self, notification_id: int, user_id: int) -> Notification | None:
        return self.db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.receiver_id == user_id
        ).first()

    def get_all_by_user_id(self, user_id: int) -> list[type[Notification]]:
        return self.db.query(Notification).filter(
            Notification.receiver_id == user_id
        ).options(
            selectinload(Notification.actor)
        ).order_by(
            Notification.created_at.desc()
        ).all()

    def get_unread_by_user_id(self, user_id: int) -> list[type[Notification]]:
        return self.db.query(Notification).filter(
            Notification.receiver_id == user_id,
            Notification.is_read == False
        ).options(
            selectinload(Notification.actor)
        ).order_by(
            Notification.created_at.desc()
        ).all()

    def mark_as_read(self, notification: Notification) -> None:
        notification.is_read = True
        self.db.commit()
        self.db.refresh(notification)
