from configs.database import get_db

from services.authentication_services import get_auth_services

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login")
async def login_for_access_token(
        data: OAuth2PasswordRequestForm = Depends(),
        db=Depends(get_db),
        auth_services=Depends(get_auth_services)
):
    return auth_services.authenticate_user(data, db)
