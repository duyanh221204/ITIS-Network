from schemas.user import UserInfoUpdateSchema
from services.profile_service import get_profile_service
from utils.configs.authentication import get_current_user
from utils.configs.database import get_db
from utils.exceptions import raise_error
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/api/profile",
    tags=["Profile"]
)


@router.get("/{user_id}")
def get_info(
        user_id: int,
        db=Depends(get_db),
        _=Depends(get_current_user),
        profile_service=Depends(get_profile_service)
):
    try:
        return profile_service.get_info(db, user_id)
    except Exception:
        return raise_error(1008)


@router.put("/update_info")
def update_info(
        data: UserInfoUpdateSchema,
        db=Depends(get_db),
        user=Depends(get_current_user),
        profile_service=Depends(get_profile_service)
):
    try:
        return profile_service.update_info(data, db, user["id"])
    except Exception:
        return raise_error(1009)
