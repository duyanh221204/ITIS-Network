from configs.database import get_db
from configs.authentication import get_current_user

from schemas.authentication import PasswordUpdateSchema
from schemas.user import UserRegisterSchema

from services.user_services import get_user_services

from exceptions import raise_error

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/user", tags=["User"])


@router.post("/register")
async def register(data: UserRegisterSchema, db=Depends(get_db), user_services=Depends(get_user_services)):
    try:
        return user_services.register(data, db)
    except Exception:
        return raise_error(1000)


@router.put("/update_password")
async def update_password(
        data: PasswordUpdateSchema,
        db=Depends(get_db),
        user=Depends(get_current_user),
        user_services=Depends(get_user_services)
):
    try:
        if user is None:
            return raise_error(1005)
        return user_services.update_password(data, db, user)
    except Exception:
        return raise_error(1005)
