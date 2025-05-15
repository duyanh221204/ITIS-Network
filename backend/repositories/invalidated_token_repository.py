from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from models import InvalidatedToken
from utils.configs.database import get_db


def get_invalidated_token_repository(db=Depends(get_db)):
    try:
        yield InvalidatedTokenRepository(db)
    finally:
        pass


class InvalidatedTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_jwt_id(self, jwt_id: str) -> InvalidatedToken | None:
        return self.db.query(InvalidatedToken).filter(InvalidatedToken.jwt_id == jwt_id).first()

    def save(self, jwt_id: str, expired_at: datetime) -> None:
        invalidated_token = InvalidatedToken(jwt_id=jwt_id, expired_at=expired_at)
        self.db.add(invalidated_token)
        self.db.commit()
        self.db.refresh(invalidated_token)
