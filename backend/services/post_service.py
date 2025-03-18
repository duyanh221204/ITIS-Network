from models.post import Post
from schemas.post import PostBaseSchema
from schemas.base_response import BaseResponse
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
