import cloudinary

from utils.constants import Constant

CLOUDINARY_CLOUD_NAME = Constant.CLOUDINARY_CLOUD_NAME
CLOUDINARY_API_KEY = Constant.CLOUDINARY_API_KEY
CLOUDINARY_API_SECRET = Constant.CLOUDINARY_API_SECRET

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)
