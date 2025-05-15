import os
from datetime import timedelta, datetime, timezone
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from repositories.invalidated_token_repository import InvalidatedTokenRepository, get_invalidated_token_repository
from schemas.authentication import TokenDataSchema

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def hash_password(plain_password: str):
    return bcrypt_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expired_delta: timedelta) -> str:
    to_encode = data.copy()
    jwt_id = str(uuid4())
    expires = datetime.now(timezone.utc) + expired_delta
    to_encode.update({"exp": expires, "id": jwt_id})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(
        token: str,
        invalidated_token_repository: InvalidatedTokenRepository
) -> TokenDataSchema | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        jwt_id: str = payload.get("id")

        if user_id is None:
            return None
        if invalidated_token_repository.get_by_jwt_id(jwt_id) is not None:
            return None

        return TokenDataSchema(id=int(user_id))
    except Exception as e:
        print ("Validating user error:\n" + str(e))
        return None


def get_current_user(
        token: str = Depends(oauth2_bearer),
        invalidated_token_repository: InvalidatedTokenRepository = Depends(get_invalidated_token_repository)
) -> TokenDataSchema | None:
    return verify_token(token, invalidated_token_repository)
