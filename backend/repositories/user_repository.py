from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User, Follow
from schemas.user import UserRegisterSchema, UserInfoUpdateSchema
from utils.configs.authentication import hash_password
from utils.configs.database import get_db


def get_user_repository(db=Depends(get_db)):
    try:
        yield UserRepository(db)
    finally:
        pass


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_username_and_id(self, username: str, user_id: int) -> User | None:
        return self.db.query(User).filter(
            User.username == username,
            User.id != user_id
        ).first()

    def get_by_email(self, email: EmailStr) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, data: UserRegisterSchema) -> None:
        new_user = User(
            username=data.username,
            email=data.email,
            avatar=data.avatar,
            introduction=data.introduction,
            hashed_password=hash_password(data.password)
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

    def update_info(self, user: User, data: UserInfoUpdateSchema) -> None:
        _data = data.model_dump(exclude_unset=True).items()
        update_data = {key: value.strip() for key, value in _data if isinstance(value, str) and value.strip() != ""}

        if update_data:
            for key, value in update_data.items():
                setattr(user, key, value)

            self.db.commit()
            self.db.refresh(user)

    def update_password(self, user: User, new_password: str) -> None:
        user.hashed_password = hash_password(new_password)
        self.db.commit()
        self.db.refresh(user)

    def follow(self, follower_id: int, followed_id: int) -> None:
        new_follow = Follow(
            follower_id=follower_id,
            followed_id=followed_id
        )
        self.db.add(new_follow)
        self.db.commit()
        self.db.refresh(new_follow)

    def unfollow(self, follower_id: int, followed_id: int) -> None:
        follow_db = self.db.query(Follow).filter(
            follower_id == follower_id,
            followed_id == followed_id
        ).first()

        self.db.delete(follow_db)
        self.db.commit()

    def get_followers(self, user_id: int) -> list[type[User]]:
        return self.db.query(User).join(
            Follow,
            Follow.follower_id == User.id
        ).filter(
            Follow.followed_id == user_id
        ).all()

    def get_followings(self, user_id: int) -> list[type[User]]:
        return self.db.query(User).join(
            Follow,
            Follow.followed_id == User.id
        ).filter(
            Follow.follower_id == user_id
        ).all()

    def get_not_following(self, user_id: int) -> list[type[User]]:
        followings = select(Follow.followed_id).where(Follow.follower_id == user_id)
        return self.db.query(User).filter(
            User.id.notin_(followings),
            User.id != user_id
        ).all()
