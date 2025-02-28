from pydantic import BaseModel
from typing import Any


class BaseResponse(BaseModel):
    status: str = "ok"
    message: str = ""
    data: Any = None
