from configs.database import get_db

from services.authentication_service import get_auth_service

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from exceptions import raise_error

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login")
async def login_for_access_token(
        data: OAuth2PasswordRequestForm = Depends(),
        db=Depends(get_db),
        auth_service=Depends(get_auth_service)
):
    try:
        return auth_service.authenticate_user(data, db)
    except Exception:
        return raise_error(1003)
