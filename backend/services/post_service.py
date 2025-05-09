from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from models import Post, Like, Comment, Follow
from schemas.base_response import BaseResponse
from schemas.comment import CommentInfoSchema, CommentBaseSchema
from schemas.like import LikeSchema
from schemas.post import PostBaseSchema, PostInfoSchema
from services.notification_service import get_notification_service
from utils.exceptions import raise_error


def get_post_service(notification_service=Depends(get_notification_service)):
    try:
        yield PostService(notification_service)
    finally:
        pass


class PostService:
    def __init__(self, notification_service):
        self.notification_service = notification_service

    def get_post_author_id(self, db: Session, post_id: int) -> int:
        return db.query(Post).filter(Post.id == post_id).first().author_id

    def create_post(self, data: PostBaseSchema, db: Session, user_id: int) -> BaseResponse:
        if data.content.strip() == "" and data.image == "":
            return raise_error(2001)

        new_post = Post(**data.model_dump(), author_id=user_id)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return BaseResponse(message="Create new post successfully")
    
    def update_post_by_id(self, data: PostBaseSchema, db: Session, post_id: int) -> BaseResponse:
        if data.content.strip() == "" and data.image == "":
            return raise_error(2001)

        post_db = db.query(Post).filter(Post.id == post_id).first()
        post_db.content = data.content
        post_db.image = data.image

        db.commit()
        db.refresh(post_db)
        return BaseResponse(message="Update post successfully")

    def delete_post_by_id(self, db: Session, post_id: int) -> BaseResponse:
        post_db = db.query(Post).filter(Post.id == post_id).first()
        db.delete(post_db)
        db.commit()
        return BaseResponse(message="Delete post successfully")
    
    def get_posts(self, query) -> BaseResponse:
        posts = query.options(
            selectinload(Post.author),
            selectinload(Post.likes).selectinload(Like.liker),
            selectinload(Post.comments).selectinload(Comment.author)
        ).order_by(Post.created_at.desc()).all()

        data = []
        for post in posts:
            likes = [
                LikeSchema(
                    id=like.id,
                    liker_id=like.liker_id,
                    liker_name=like.liker.username,
                    liker_avatar=like.liker.avatar,
                    post_id=post.id
                )
                for like in post.likes
            ]

            comments = [
                CommentInfoSchema(
                    id=comment.id,
                    content=comment.content,
                    author_id=comment.author_id,
                    author_name=comment.author.username,
                    author_avatar=comment.author.avatar,
                    post_id=post.id
                )
                for comment in post.comments
            ]

            data.append(PostInfoSchema(
                id=post.id,
                content=post.content,
                image=post.image,
                author_id=post.author_id,
                author_name=post.author.username,
                author_avatar=post.author.avatar,
                created_at=post.created_at,
                likes=likes,
                comments=comments
            ))

        return BaseResponse(message="Posts retrieved successfully", data=data)

    def get_all_posts(self, db: Session) -> BaseResponse:
        return self.get_posts(db.query(Post))

    def get_posts_by_followings(self, db: Session, user_id: int) -> BaseResponse:
        followings = select(Follow.followed_id).where(Follow.follower_id == user_id)
        return self.get_posts(db.query(Post).filter(Post.author_id.in_(followings)))

    def get_posts_by_user(self, db: Session, user_id: int) -> BaseResponse:
        return self.get_posts(db.query(Post).filter(Post.author_id == user_id))

    def like_post(self, db: Session, liker_id: int, post_id: int) -> BaseResponse:
        new_like = Like(
            liker_id=liker_id,
            post_id=post_id
        )

        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return BaseResponse(message="Like post successfully")

    def unlike_post(self, db: Session, liker_id: int, post_id: int) -> BaseResponse:
        like_db = db.query(Like).filter(
            liker_id == liker_id,
            post_id == post_id
        ).first()

        db.delete(like_db)
        db.commit()
        return BaseResponse(message="Unlike post successfully")

    def create_comment(self, data: CommentBaseSchema, db: Session, author_id: int) -> BaseResponse:
        if data.content.strip() == "":
            return raise_error(2006)

        new_comment = Comment(**data.model_dump(), author_id=author_id)
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return BaseResponse(message="Create comment successfully")

    def delete_comment(self, db: Session, comment_id: int, author_id: int) -> BaseResponse:
        comment_db = db.query(Comment).filter(
            Comment.id == comment_id,
            Comment.author_id == author_id
        ).first()
        db.delete(comment_db)
        db.commit()
        return BaseResponse(message="Delete comment successfully")
