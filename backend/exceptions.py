from schemas.base_response import BaseResponse
from typing import Any

ERROR_CODES = {
    1000: "Registration error",
    1001: "Username existed",
    1002: "Email existed",
    1003: "Login failed",
    1004: "Incorrect credentials",
    1005: "Incorrect current password",
    1006: "Error updating password",
    1007: "Unable to get user's info",

    2000: "Error uploading image"
}


def raise_error(error_code: int, data: Any = None) -> BaseResponse:
    return BaseResponse(status="error", message=ERROR_CODES[error_code], data=data)
