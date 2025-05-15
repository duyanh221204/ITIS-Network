from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from models import Post, Like, Comment, Follow
from schemas.comment import CommentBaseSchema
from schemas.post import PostBaseSchema
from utils.configs.database import get_db


def get_post_repository(db=Depends(get_db)):
    try:
        yield PostRepository(db)
    finally:
        pass


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, post_id: int) -> Post | None:
        return self.db.query(Post).filter(Post.id == post_id).first()

    def create(self, data: PostBaseSchema, author_id: int) -> None:
        new_post = Post(**data.model_dump(), author_id=author_id)
        self.db.add(new_post)
        self.db.commit()
        self.db.refresh(new_post)

    def update(self, data: PostBaseSchema, post: Post) -> None:
        post.content = data.content
        post.image = data.image

        self.db.commit()
        self.db.refresh(post)

    def delete(self, post: Post) -> None:
        self.db.delete(post)
        self.db.commit()

    def get_all(self) -> list[type[Post]]:
        return self.db.query(Post).options(
            selectinload(Post.author),
            selectinload(Post.likes).selectinload(Like.liker),
            selectinload(Post.comments).selectinload(Comment.author)
        ).order_by(
            Post.created_at.desc()
        ).all()

    def get_by_followings(self, user_id: int) -> list[type[Post]]:
        followings = select(Follow.followed_id).where(Follow.follower_id == user_id)
        return self.db.query(Post).filter(
            Post.author_id.in_(followings)
        ).options(
            selectinload(Post.author),
            selectinload(Post.likes).selectinload(Like.liker),
            selectinload(Post.comments).selectinload(Comment.author)
        ).order_by(
            Post.created_at.desc()
        ).all()

    def get_by_not_followings(self, user_id: int) -> list[type[Post]]:
        followings = select(Follow.followed_id).where(Follow.follower_id == user_id)
        return self.db.query(Post).filter(
            Post.author_id.notin_(followings)
        ).options(
            selectinload(Post.author),
            selectinload(Post.likes).selectinload(Like.liker),
            selectinload(Post.comments).selectinload(Comment.author)
        ).order_by(
            Post.created_at.desc()
        ).all()

    def get_by_user_id(self, user_id: int) -> list[type[Post]]:
        return self.db.query(Post).filter(
            Post.author_id == user_id
        ).options(
            selectinload(Post.author),
            selectinload(Post.likes).selectinload(Like.liker),
            selectinload(Post.comments).selectinload(Comment.author)
        ).order_by(
            Post.created_at.desc()
        ).all()

    def like(self, liker_id: int, post_id: int) -> Like:
        new_like = Like(
            liker_id=liker_id,
            post_id=post_id
        )

        self.db.add(new_like)
        self.db.commit()
        self.db.refresh(new_like)
        return new_like

    def unlike(self, liker_id: int, post_id: int) -> None:
        like_db = self.db.query(Like).filter(
            liker_id == liker_id,
            post_id == post_id
        ).first()

        self.db.delete(like_db)
        self.db.commit()

    def comment(self, data: CommentBaseSchema, author_id: int) -> Comment:
        new_comment = Comment(**data.model_dump(), author_id=author_id)
        self.db.add(new_comment)
        self.db.commit()
        self.db.refresh(new_comment)
        return new_comment

    def delete_comment(self, comment_id: int, author_id: int) -> None:
        comment_db = self.db.query(Comment).filter(
            Comment.id == comment_id,
            Comment.author_id == author_id
        ).first()
        self.db.delete(comment_db)
        self.db.commit()
