from configs.database import get_db

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
