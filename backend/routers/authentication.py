from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from schemas.authentication import OTPRequestSchema, PasswordResetSchema
from schemas.user import UserRegisterSchema
from services.authentication_service import get_auth_service, AuthenticationService
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
