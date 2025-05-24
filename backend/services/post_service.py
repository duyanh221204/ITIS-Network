from fastapi import Depends

from models import Post
from repositories.post_repository import get_post_repository, PostRepository
from schemas.base_response import BaseResponse
from schemas.comment import CommentInfoSchema, CommentBaseSchema
from schemas.hashtag import HashtagSchema
from schemas.like import LikeSchema
from schemas.post import PostInfoSchema, PostCreateSchema, PostUpdateSchema
from services.notification_service import get_notification_service, NotificationService
from utils.exceptions import raise_error


def get_post_service(
        post_repository=Depends(get_post_repository),
        notification_service=Depends(get_notification_service)
):
    try:
        yield PostService(post_repository, notification_service)
    finally:
        pass


class PostService:
    def __init__(self, post_repository: PostRepository, notification_service: NotificationService):
        self.post_repository = post_repository
        self.notification_service = notification_service

    def create_post(self, data: PostCreateSchema, user_id: int) -> BaseResponse:
        if data.content.strip() == "" and data.image == "":
            return raise_error(2001)

        self.post_repository.create(data, user_id)
        return BaseResponse(message="Create new post successfully")
    
    def update_post_by_id(self, data: PostUpdateSchema, post_id: int) -> BaseResponse:
        if data.content.strip() == "" and data.image == "":
            return raise_error(2001)

        post_db = self.post_repository.get_by_id(post_id)
        self.post_repository.update(data, post_db)
        return BaseResponse(message="Update post successfully")

    def delete_post_by_id(self, post_id: int) -> BaseResponse:
        post_db = self.post_repository.get_by_id(post_id)
        self.post_repository.delete(post_db)
        return BaseResponse(message="Delete post successfully")
    
    def get_posts(self, posts: list[type[Post]]) -> BaseResponse:
        data = []
        for post in posts:
            likes = [
                LikeSchema(
                    id=like.id,
                    liker_id=like.liker_id,
                    liker_name=like.liker.username,
                    liker_avatar=like.liker.avatar,
                    post_id=post.id,
                    post_author_id=post.author_id
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
                    post_id=post.id,
                    post_author_id=post.author_id
                )
                for comment in post.comments
            ]
            
            hashtags = [
                HashtagSchema(
                    id=post_hashtag.hashtag.id,
                    name=post_hashtag.hashtag.name
                )
                for post_hashtag in post.hashtags
            ]

            data.append(PostInfoSchema(
                id=post.id,
                content=post.content,
                image=post.image,
                hashtags=hashtags,
                author_id=post.author_id,
                author_name=post.author.username,
                author_avatar=post.author.avatar,
                created_at=post.created_at,
                likes=likes,
                comments=comments
            ))

        return BaseResponse(message="Posts retrieved successfully", data=data)

    def get_all_posts(self) -> BaseResponse:
        posts = self.post_repository.get_all()
        return self.get_posts(posts)

    def get_posts_by_followings(self, user_id: int) -> BaseResponse:
        posts = self.post_repository.get_by_followings(user_id)
        return self.get_posts(posts)
    
    def get_posts_by_not_followings(self, user_id: int) -> BaseResponse:
        posts = self.post_repository.get_by_not_followings(user_id)
        return self.get_posts(posts)

    def get_posts_by_user(self, user_id: int) -> BaseResponse:
        posts = self.post_repository.get_by_user_id(user_id)
        return self.get_posts(posts)

    def get_posts_by_hashtag(self, hashtag: str) -> BaseResponse:
        posts = self.post_repository.get_by_hashtag(hashtag)
        return self.get_posts(posts)

    def like_post(self, liker_id: int, post_id: int) -> BaseResponse:
        new_like = self.post_repository.like(liker_id, post_id)
        data = LikeSchema(
            id=new_like.id,
            liker_id=new_like.liker_id,
            liker_name=new_like.liker.username,
            liker_avatar=new_like.liker.avatar,
            post_id=new_like.post_id,
            post_author_id=new_like.post.author_id
        )
        return BaseResponse(message="Like post successfully", data=data)

    def unlike_post(self, liker_id: int, post_id: int) -> BaseResponse:
        self.post_repository.unlike(liker_id, post_id)
        return BaseResponse(message="Unlike post successfully")

    def create_comment(self, data: CommentBaseSchema, author_id: int) -> BaseResponse:
        if data.content.strip() == "":
            return raise_error(2006)

        new_comment = self.post_repository.comment(data, author_id)
        data = CommentInfoSchema(
            id=new_comment.id,
            content=new_comment.content,
            author_id=new_comment.author_id,
            author_name=new_comment.author.username,
            author_avatar=new_comment.author.avatar,
            post_id=new_comment.post_id,
            post_author_id=new_comment.post.author_id
        )
        return BaseResponse(message="Create comment successfully", data=data)

    def delete_comment(self, comment_id: int, author_id: int) -> BaseResponse:
        self.post_repository.delete_comment(comment_id, author_id)
        return BaseResponse(message="Delete comment successfully")
