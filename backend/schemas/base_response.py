from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: str = "ok"
    message: str = ""
    data: Any = None
