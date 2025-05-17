from fastapi import Depends

from models.notification import NotificationType
from repositories.notification_repository import NotificationRepository, get_notification_repository
from schemas.base_response import BaseResponse
from schemas.notification import NotificationSchema
from schemas.user import UserMiniSchema
from utils.exceptions import raise_error


def get_notification_service(notification_repository=Depends(get_notification_repository)):
    try:
        yield NotificationService(notification_repository)
    finally:
        pass


class NotificationService:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    def notify(
            self, actor_id: int, receiver_id: int, noti_type: NotificationType, post_id: int | None = None
    ) -> BaseResponse:
        noti = self.notification_repository.create(actor_id, receiver_id, noti_type, post_id)
        new_noti = self.notification_repository.get_by_id(noti.id)
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
                created_at=noti.created_at,
            )
            for noti in notis
        ]
        return BaseResponse(message="All notifications retrieved", data=data)

    def get_all_notifications(self, user_id: int) -> BaseResponse:
        notis = self.notification_repository.get_all_by_user_id(user_id)
        return self.get_notifications(notis)

    def get_unread_notifications(self, user_id: int) -> BaseResponse:
        unread_notis = self.notification_repository.get_unread_by_user_id(user_id)
        return self.get_notifications(unread_notis)

    def mark_as_read(self, user_id: int, noti_id: int) -> BaseResponse:
        noti = self.notification_repository.get_by_id_and_user_id(noti_id, user_id)
        if noti is None:
            return raise_error(3001)

        self.notification_repository.mark_as_read(noti)
        return BaseResponse(message="Marked notification as read")
