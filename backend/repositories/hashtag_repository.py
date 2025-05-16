from fastapi import Depends
from sqlalchemy.orm import Session

from models import Hashtag
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
        return self.db.query(Hashtag).order_by(Hashtag.created_at.desc()).all()

    def get_or_create(self, names: list[str]) -> dict[str, Hashtag]:
        existing_hashtags = self.db.query(Hashtag).filter(Hashtag.name.in_(names)).all()
        existing_map = {hashtag.name: hashtag for hashtag in existing_hashtags}

        to_create = set(names) - existing_map.keys()
        if to_create:
            new_hashtags = [Hashtag(name=name) for name in to_create]
            self.db.add_all(new_hashtags)
            self.db.flush()

            for hashtag in new_hashtags:
                existing_map[hashtag.name] = hashtag

        return existing_map
