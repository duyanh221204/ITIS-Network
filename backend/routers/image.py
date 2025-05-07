from fastapi import APIRouter, UploadFile, File, Depends

from services.image_service import get_image_service
from utils.exceptions import raise_error

router = APIRouter(
    prefix="/api/images",
    tags=["Image"]
)


@router.post("/upload")
async def upload_image(
        data: UploadFile = File(...),
        image_service=Depends(get_image_service)
):
    try:
        return image_service.upload_image(data)
    except Exception:
        return raise_error(2000)
