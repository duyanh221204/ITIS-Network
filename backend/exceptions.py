from schemas.base_response import BaseResponse
from typing import Any

ERROR_CODES = {
    1000: "Registration error",
    1001: "Username existed",
    1002: "Email existed",
}


def raise_error(error_code: int, data: Any = None) -> BaseResponse:
    return BaseResponse(
        status="error",
        message=ERROR_CODES[error_code],
        data=data
    )
