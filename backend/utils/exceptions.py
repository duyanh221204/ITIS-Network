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
    1010: "Error following user",
    1011: "Error unfollowing user",
    1012: "Error retrieving users",

    2000: "Error uploading image",
    2001: "Post must have content or image",
    2002: "Error creating new post",
    2003: "Error updating post",
    2004: "Error deleting post",
    2005: "Error retrieving posts",
    2006: "Comment must have content",
    2007: "Error liking post",
    2008: "Error unliking post",
    2009: "Error creating comment",
    2010: "Error deleting comment",

    3000: "Error retrieving all notifications",
    3001: "Notification not found",
    3002: "Error marking notification as read",

    4000: "Error creating conversation",
    4001: "Error retrieving conversations",
    4002: "Error retrieving messages or no access",
    4003: "Error sending message",
    4004: "Error marking conversation as read",
    4005: "Error retrieving unread conversations",

    5000: "Error sending OTP",
}


def raise_error(error_code: int) -> BaseResponse:
    return BaseResponse(
        status="error",
        message=ERROR_CODES[error_code]
    )
