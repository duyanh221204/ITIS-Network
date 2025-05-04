from datetime import datetime

from pydantic import BaseModel

from schemas.user import UserMiniSchema


class NotificationSchema(BaseModel):
    id: int
    actor: UserMiniSchema | None
    type: str
    post_id: int | None = None
    is_read: bool
    created_at: datetime

    model_config = {
        "from_attribute": True
    }
