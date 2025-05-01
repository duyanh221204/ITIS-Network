from schemas.base_response import BaseResponse
from utils.exceptions import raise_error
from fastapi import UploadFile
import cloudinary
from cloudinary.uploader import upload
from dotenv import load_dotenv
import os

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


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
