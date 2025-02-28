from configs.database import get_db
from configs.authentication import get_current_user

from schemas.authentication import PasswordUpdateSchema
from schemas.user import UserRegisterSchema

from services.user_service import get_user_service

from exceptions import raise_error

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/user", tags=["User"])


@router.post("/register")
async def register(
        data: UserRegisterSchema,
        db=Depends(get_db),
        user_service=Depends(get_user_service)
):
    try:
        return user_service.register(data, db)
    except Exception:
        return raise_error(1000)


@router.get("/info")
async def get_info(
        db=Depends(get_db),
        user=Depends(get_current_user),
        user_service=Depends(get_user_service)
):
    try:
        return user_service.get_info(db, user)
    except Exception:
        return raise_error(1007)


@router.put("/update_password")
async def update_password(
        data: PasswordUpdateSchema,
        db=Depends(get_db),
        user=Depends(get_current_user),
        user_service=Depends(get_user_service)
):
    try:
        return user_service.update_password(data, db, user)
    except Exception:
        return raise_error(1006)
