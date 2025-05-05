import utils.configs.cloudinary

from cloudinary.uploader import upload
from fastapi import UploadFile

from schemas.base_response import BaseResponse
from utils.exceptions import raise_error


def get_image_service():
    try:
        yield ImageService()
    finally:
        pass


class ImageService:
    def upload_image(self, data: UploadFile) -> BaseResponse:
        try:
            result = upload(data.file)
            image_url = result["secure_url"]
            return BaseResponse(message="Upload image successfully", data=image_url)
        except Exception:
            return raise_error(2000)
