from fastapi import APIRouter, Depends, BackgroundTasks

from models.notification import NotificationType
from schemas.comment import CommentBaseSchema
from schemas.post import PostBaseSchema
from services.post_service import get_post_service
from utils.configs.authentication import get_current_user
from utils.configs.database import get_db
from utils.exceptions import raise_error

router = APIRouter(
    prefix="/api/posts",
    tags=["Post"]
)


@router.get("/all")
async def get_all_posts(
        db=Depends(get_db),
        user=Depends(get_current_user),
        post_service=Depends(get_post_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return post_service.get_all_posts(db)
    except Exception:
        return raise_error(2005)


@router.get("/followings")
async def get_posts_by_followings(
        db=Depends(get_db),
        user=Depends(get_current_user),
        post_service=Depends(get_post_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return post_service.get_posts_by_followings(db, user["id"])
    except Exception:
        return raise_error(2005)


@router.get("/user/{user_id}")
async def get_posts_by_user(
        user_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        post_service=Depends(get_post_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return post_service.get_posts_by_user(db, user_id)
    except Exception:
        return raise_error(2005)


@router.post("/create")
async def create_post(
        data: PostBaseSchema,
        db=Depends(get_db),
        user=Depends(get_current_user),
        post_service=Depends(get_post_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return post_service.create_post(data, db, user["id"])
    except Exception:
        return raise_error(2002)


@router.put("/update/{post_id}")
async def update_post_by_id(
        data: PostBaseSchema,
        post_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        post_service=Depends(get_post_service),
):
    try:
        if user is None:
            return raise_error(1005)
        return post_service.update_post_by_id(data, db, post_id)
    except Exception:
        return raise_error(2003)


@router.delete("/delete/{post_id}")
async def delete_post_by_id(
        post_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        post_service=Depends(get_post_service),
):
    try:
        if user is None:
            return raise_error(1005)
        return post_service.delete_post_by_id(db, post_id)
    except Exception:
        return raise_error(2004)


@router.post("/like/{post_id}")
async def like_post(
        post_id: int,
        background_tasks: BackgroundTasks,
        db=Depends(get_db),
        user=Depends(get_current_user),
        post_service=Depends(get_post_service)
):
    try:
        if user is None:
            return raise_error(1005)

        response = post_service.like_post(db, user["id"], post_id)
        if response.status == "ok":
            background_tasks.add_task(
                post_service.notification_service.notify,
                db,
                user["id"],
                post_service.get_post_author_id(db, post_id),
                NotificationType.LIKE,
                post_id
            )
        return response
    except Exception:
        return raise_error(2007)


@router.delete("/unlike/{post_id}")
async def unlike_post(
        post_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        post_service=Depends(get_post_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return post_service.unlike_post(db, user["id"], post_id)
    except Exception:
        return raise_error(2008)


@router.post("/create_comment/{post_id}")
async def create_comment(
        data: CommentBaseSchema,
        background_tasks: BackgroundTasks,
        db=Depends(get_db),
        user=Depends(get_current_user),
        post_service=Depends(get_post_service)
):
    try:
        if user is None:
            return raise_error(1005)

        response = post_service.create_comment(data, db, user["id"])
        if response.status == "ok":
            background_tasks.add_task(
                post_service.notification_service.notify,
                db,
                user["id"],
                post_service.get_post_author_id(db, data.post_id),
                NotificationType.COMMENT,
                data.post_id
            )
        return response
    except Exception:
        return raise_error(2009)


@router.delete("/delete_comment/{comment_id}")
async def delete_comment(
        comment_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        post_service=Depends(get_post_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return post_service.delete_comment(db, comment_id, user["id"])
    except Exception:
        return raise_error(2010)
