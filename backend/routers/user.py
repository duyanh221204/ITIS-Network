from schemas.user import UserInfoUpdateSchema, UserPasswordUpdateSchema
from services.user_service import get_user_service
from utils.configs.authentication import get_current_user
from utils.configs.database import get_db
from utils.exceptions import raise_error
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/api/user",
    tags=["User"]
)


@router.get("/info")
def get_info(
        db=Depends(get_db),
        user=Depends(get_current_user),
        user_service=Depends(get_user_service)
):
    try:
        return user_service.get_info(db, user["id"])
    except Exception:
        return raise_error(1008)


@router.put("/update_info")
def update_info(
        data: UserInfoUpdateSchema,
        db=Depends(get_db),
        user=Depends(get_current_user),
        user_service=Depends(get_user_service)
):
    try:
        return user_service.update_info(data, db, user["id"])
    except Exception:
        return raise_error(1009)


@router.put("/update_password")
def update_password(
        data: UserPasswordUpdateSchema,
        db=Depends(get_db),
        user=Depends(get_current_user),
        user_service=Depends(get_user_service)
):
    try:
        return user_service.update_password(data, db, user["id"])
    except Exception:
        return raise_error(1007)
