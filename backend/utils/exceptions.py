from schemas.base_response import BaseResponse

ERROR_CODES = {
    1000: "Registration error",
    1001: "Username existed",
    1002: "Email existed",
    1003: "Login failed",
    1004: "Incorrect credentials",
    1005: "Unable to validate user",
    1006: "Incorrect current password",
    1007: "Error updating password",
    1008: "Error getting user's info",
    1009: "Error updating user's info",

    2000: "Error uploading image",
    2001: "Post must have content or image",
    2002: "Error creating new post",
    2003: "Error updating post",
    2004: "Error deleting post"
}


def raise_error(error_code: int) -> BaseResponse:
    return BaseResponse(
        status="error",
        message=ERROR_CODES[error_code]
    )
