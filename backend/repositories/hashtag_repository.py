from fastapi import Depends
from sqlalchemy.orm import Session

from models import Hashtag
from schemas.hashtag import HashTagCreateSchema
from utils.configs.database import get_db


def get_hashtag_repository(db=Depends(get_db)):
    try:
        yield HashtagRepository(db)
    finally:
        pass


class HashtagRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Hashtag | None:
        return self.db.query(Hashtag).filter(Hashtag.name == name).first()

    def get_all(self) -> list[type[Hashtag]]:
        return self.db.query(Hashtag).all()

    def create(self, data: HashTagCreateSchema) -> Hashtag:
        new_hashtag = Hashtag(name=data.name.strip().replace(" ", ""))

        self.db.add(new_hashtag)
        self.db.commit()
        self.db.refresh(new_hashtag)
        return new_hashtag
