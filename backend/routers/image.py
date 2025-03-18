from services.image_service import get_image_service
from utils.configs.authentication import get_current_user
from utils.exceptions import raise_error
from fastapi import APIRouter, Depends, UploadFile, File

router = APIRouter(
    prefix="/api/image",
    tags=["Image"]
)


@router.post("/upload")
def upload_image(
        data: UploadFile = File(...),
        _=Depends(get_current_user),
        image_service=Depends(get_image_service)
):
    try:
        return image_service.upload_image(data)
    except Exception:
        return raise_error(2000)
