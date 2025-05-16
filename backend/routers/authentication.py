from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from schemas.authentication import OTPRequestSchema, PasswordResetSchema, TokenDataSchema
from schemas.user import UserRegisterSchema
from services.authentication_service import get_auth_service, AuthenticationService
from utils.configs.authentication import get_current_user, oauth2_bearer
from utils.exceptions import raise_error

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register")
async def register(
        data: UserRegisterSchema,
        auth_service: AuthenticationService = Depends(get_auth_service)
):
    try:
        return auth_service.register(data)
    except Exception as e:
        print ("Registration error:\n" + str(e))
        return raise_error(1000)


@router.post("/login")
async def login_for_access_token(
        data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthenticationService = Depends(get_auth_service)
):
    try:
        return auth_service.authenticate_user(data)
    except Exception as e:
        print ("Login error:\n" + str(e))
        return raise_error(1003)
    
    
@router.post("/otp")
async def send_otp(
        data: OTPRequestSchema,
        auth_service: AuthenticationService = Depends(get_auth_service)
):
    try:
        return auth_service.send_otp(data)
    except Exception as e:
        print ("Sending OTP error:\n" + str(e))
        return raise_error(5000)


@router.put("/reset-password")
async def reset_password(
        data: PasswordResetSchema,
        auth_service: AuthenticationService = Depends(get_auth_service)
):
    try:
        return auth_service.reset_password(data)
    except Exception as e:
        print ("Reset password error:\n" + str(e))
        return raise_error(1007)


@router.post("/refresh")
async def refresh_token(
        token: str = Depends(oauth2_bearer),
        user: TokenDataSchema = Depends(get_current_user),
        auth_service: AuthenticationService = Depends(get_auth_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return auth_service.refresh_token(token)
    except Exception as e:
        print ("Refresh token error:\n" + str(e))
        return raise_error(1013)


@router.post("/logout")
async def logout(
        token: str = Depends(oauth2_bearer),
        user: TokenDataSchema = Depends(get_current_user),
        auth_service: AuthenticationService = Depends(get_auth_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return auth_service.logout(token)
    except Exception as e:
        print ("Logout error:\n" + str(e))
        return raise_error(1014)
