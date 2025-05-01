from models.follow import Follow
from models.notification import Notification, NotificationType
from models.post import Post
from models.like import Like
from models.comment import Comment
from models.user import User
from schemas.post import PostBaseSchema, PostInfoSchema
from schemas.base_response import BaseResponse
from schemas.comment import CommentBaseSchema, CommentInfoSchema
from schemas.like import LikeSchema
from utils.exceptions import raise_error
from sqlalchemy.orm import Session


def get_post_service():
    try:
        yield PostService()
    finally:
        pass


class PostService:
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

    def get_all_posts(self, db: Session) -> BaseResponse:
        posts_db = db.query(Post).all()
        posts_data = []

        for post in posts_db:
            likes = db.query(Like).filter(Like.post_id == post.id).all()
            likes_data = []
            for like in likes:
                liker = db.query(User).filter(User.id == like.liker_id).first()
                likes_data.append(
                    LikeSchema(
                        id=like.id,
                        liker_id=liker.id,
                        liker_name=liker.username,
                        liker_avatar=liker.avatar,
                        post_id=post.id
                    )
                )

            comments = db.query(Comment).filter(Comment.post_id == post.id).all()
            comments_data = []
            for comment in comments:
                author = db.query(User).filter(User.id == comment.author_id).first()
                comments_data.append(
                    CommentInfoSchema(
                        id=comment.id,
                        content=comment.content,
                        author_id=author.id,
                        author_name=author.username,
                        author_avatar=author.avatar,
                        post_id=post.id
                    )
                )
            
            author = db.query(User).filter(User.id == post.author_id).first()
            posts_data.append(
                PostInfoSchema(
                    id=post.id,
                    content=post.content,
                    image=post.image,
                    author_id=author.id,
                    author_name=author.username,
                    author_avatar=author.avatar,
                    created_at=post.created_at,
                    likes=likes_data,
                    comments=comments_data
                )
            )
        return BaseResponse(message="Posts retrieved successfully", data=posts_data)

    def get_posts_by_followings(self, db: Session, user_id: int) -> BaseResponse:
        followed = db.query(Follow.followed_id).filter(Follow.follower_id == user_id).all()
        followed_ids = [result[0] for result in followed]

        posts_db = db.query(Post).filter(Post.author_id.in_(followed_ids)).all()
        posts_data = []
        for post in posts_db:
            likes = db.query(Like).filter(Like.post_id == post.id).all()
            likes_data = []
            for like in likes:
                liker = db.query(User).filter(User.id == like.liker_id).first()
                likes_data.append(
                    LikeSchema(
                        id=like.id,
                        liker_id=liker.id,
                        liker_name=liker.username,
                        liker_avatar=liker.avatar,
                        post_id=post.id
                    )
                )

            comments = db.query(Comment).filter(Comment.post_id == post.id).all()
            comments_data = []
            for comment in comments:
                author = db.query(User).filter(User.id == comment.author_id).first()
                comments_data.append(
                    CommentInfoSchema(
                        id=comment.id,
                        content=comment.content,
                        author_id=author.id,
                        author_name=author.username,
                        author_avatar=author.avatar,
                        post_id=post.id
                    )
                )

            author = db.query(User).filter(User.id == post.author_id).first()
            posts_data.append(
                PostInfoSchema(
                    id=post.id,
                    content=post.content,
                    image=post.image,
                    author_id=author.id,
                    author_name=author.username,
                    author_avatar=author.avatar,
                    created_at=post.created_at,
                    likes=likes_data,
                    comments=comments_data
                )
            )
        return BaseResponse(message="Posts retrieved successfully", data=posts_data)


    def get_posts_by_user(self, db: Session, user_id: int) -> BaseResponse:
        posts_db = db.query(Post).filter(Post.author_id == user_id).all()
        posts_author = db.query(User).filter(User.id == user_id).first()
        posts_data = []

        for post in posts_db:
            likes = db.query(Like).filter(Like.post_id == post.id).all()
            likes_data = []
            for like in likes:
                liker = db.query(User).filter(User.id == like.liker_id).first()
                likes_data.append(
                    LikeSchema(
                        id=like.id,
                        liker_id=liker.id,
                        liker_name=liker.username,
                        liker_avatar=liker.avatar,
                        post_id=post.id
                    )
                )

            comments = db.query(Comment).filter(Comment.post_id == post.id).all()
            comments_data = []
            for comment in comments:
                author = db.query(User).filter(User.id == comment.author_id).first()
                comments_data.append(
                    CommentInfoSchema(
                        id=comment.id,
                        content=comment.content,
                        author_id=author.id,
                        author_name=author.username,
                        author_avatar=author.avatar,
                        post_id=post.id
                    )
                )

            posts_data.append(
                PostInfoSchema(
                    id=post.id,
                    content=post.content,
                    image=post.image,
                    author_id=posts_author.id,
                    author_name=posts_author.username,
                    author_avatar=posts_author.avatar,
                    created_at=post.created_at,
                    likes=likes_data,
                    comments=comments_data
                )
            )
        return BaseResponse(message="Posts retrieved successfully", data=posts_data)


    def like_post(self, db: Session, liker_id: int, post_id: int) -> BaseResponse:
        new_like = Like(
            liker_id=liker_id,
            post_id=post_id
        )

        db.add(new_like)

        post = db.query(Post).filter(Post.id == post_id).first()
        if post.author_id != liker_id:
            db.add(Notification(
                type=NotificationType.LIKE,
                actor_id=liker_id,
                receiver_id=post.author_id,
                post_id=post_id
            ))

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

        post = db.query(Post).filter(Post.id == data.post_id).first()
        if post.author_id != author_id:
            db.add(Notification(
                type=NotificationType.COMMENT,
                actor_id=author_id,
                receiver_id=post.author_id,
                post_id=data.post_id
            ))

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
