from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, Query

from models import Post, Like, Comment, Follow, PostHashtag
from repositories.hashtag_repository import HashtagRepository, get_hashtag_repository
from schemas.comment import CommentBaseSchema
from schemas.post import PostCreateSchema, PostUpdateSchema
from configs.database import get_db


def get_post_repository(db=Depends(get_db), hashtag_repository=Depends(get_hashtag_repository)):
    try:
        yield PostRepository(db, hashtag_repository)
    finally:
        pass


class PostRepository:
    def __init__(self, db: Session, hashtag_repository: HashtagRepository):
        self.db = db
        self.hashtag_repository = hashtag_repository

    def base_query(self) -> Query[type[Post]]:
        return self.db.query(Post).options(
            selectinload(Post.author),
            selectinload(Post.likes).selectinload(Like.liker),
            selectinload(Post.comments).selectinload(Comment.author),
            selectinload(Post.hashtags).selectinload(PostHashtag.hashtag)
        )

    def get_by_id(self, post_id: int) -> Post | None:
        return self.base_query().filter(
            Post.id == post_id
        ).first()

    def create(self, data: PostCreateSchema, author_id: int) -> None:
        new_post = Post(
            content=data.content,
            image=data.image,
            author_id=author_id
        )

        hashtags = data.hashtags
        if hashtags:
            all_hashtags = self.hashtag_repository.get_or_create(hashtags)
            new_post.hashtags = [
                PostHashtag(hashtag_id=all_hashtags[hashtag].id) for hashtag in hashtags
            ]

        self.db.add(new_post)
        self.db.commit()
        self.db.refresh(new_post)

    def update(self, data: PostUpdateSchema, post: Post) -> None:
        post.content = data.content
        post.image = data.image

        hashtags = data.hashtags
        all_hashtags = self.hashtag_repository.get_or_create(hashtags)

        current = {post_hashtag.hashtag.name: post_hashtag for post_hashtag in post.hashtags}
        for name, post_hashtag in current.items():
            if name not in hashtags:
                post.hashtags.remove(post_hashtag)
                self.db.delete(post_hashtag)
                
        for hashtag in hashtags:
            if hashtag not in current:
                post_hashtag = PostHashtag(
                    post_id=post.id,
                    hashtag_id=all_hashtags[hashtag].id
                )
                post.hashtags.append(post_hashtag)

        self.db.commit()
        self.db.refresh(post)

    def delete(self, post: Post) -> None:
        self.db.delete(post)
        self.db.commit()

    def get_all(self) -> list[type[Post]]:
        return self.base_query().order_by(
            Post.created_at.desc()
        ).all()

    def get_by_followings(self, user_id: int) -> list[type[Post]]:
        followings = select(Follow.followed_id).where(Follow.follower_id == user_id)
        return self.base_query().filter(
            Post.author_id.in_(followings)
        ).order_by(
            Post.created_at.desc()
        ).all()

    def get_by_not_followings(self, user_id: int) -> list[type[Post]]:
        followings = select(Follow.followed_id).where(Follow.follower_id == user_id)
        return self.base_query().filter(
            Post.author_id.notin_(followings)
        ).order_by(
            Post.created_at.desc()
        ).all()

    def get_by_user_id(self, user_id: int) -> list[type[Post]]:
        return self.base_query().filter(
            Post.author_id == user_id
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
            Like.liker_id == liker_id,
            Like.post_id == post_id
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
