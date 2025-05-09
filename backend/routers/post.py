from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from models.notification import NotificationType
from schemas.comment import CommentBaseSchema
from schemas.post import PostBaseSchema
from services.post_service import get_post_service
from utils.configs.authentication import get_current_user
from utils.configs.database import get_db
from utils.configs.websocket import websocket_manager
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
    except Exception as e:
        print ("Getting all posts error:\n", str(e))
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
        return post_service.get_posts_by_followings(db, user.get("id"))
    except Exception as e:
        print ("Getting following posts error:\n", str(e))
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
    except Exception as e:
        print ("Getting user's posts error:\n", str(e))
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
        return post_service.create_post(data, db, user.get("id"))
    except Exception as e:
        print ("Creating new post error:\n", str(e))
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
    except Exception as e:
        print ("Updating post error:\n", str(e))
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
    except Exception as e:
        print ("Deleting post error:\n", str(e))
        return raise_error(2004)


@router.post("/like/{post_id}")
async def like_post(
        post_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        post_service=Depends(get_post_service)
):
    try:
        if user is None:
            return raise_error(1005)

        response = post_service.like_post(db, user.get("id"), post_id)
        if response.status == "ok":
            receiver_id = post_service.get_post_author_id(db, post_id)
            noti = post_service.notification_service.notify(
                db,
                user.get("id"),
                receiver_id,
                NotificationType.LIKE,
                post_id
            )

            if noti.status == "ok":
                new_noti = noti.data
                payload: dict = {
                    "type": "new_notification",
                    "data": {
                        "id": new_noti.id,
                        "type": new_noti.type,
                        "is_read": new_noti.is_read,
                        "created_at": new_noti.created_at.isoformat(),
                        "post_id": post_id,
                        "actor_id": new_noti.actor.id,
                    }
                }

                await websocket_manager.broadcast(receiver_id, jsonable_encoder(payload))
        return response
    except Exception as e:
        print ("Like post error:\n", str(e))
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
        return post_service.unlike_post(db, user.get("id"), post_id)
    except Exception as e:
        print ("Unlike post error:\n", str(e))
        return raise_error(2008)


@router.post("/create-comment/{post_id}")
async def create_comment(
        data: CommentBaseSchema,
        db=Depends(get_db),
        user=Depends(get_current_user),
        post_service=Depends(get_post_service)
):
    try:
        if user is None:
            return raise_error(1005)

        response = post_service.create_comment(data, db, user.get("id"))
        if response.status == "ok":
            receiver_id = post_service.get_post_author_id(db, data.post_id)
            noti = post_service.notification_service.notify(
                db,
                user.get("id"),
                receiver_id,
                NotificationType.LIKE,
                data.post_id
            )

            if noti.status == "ok":
                new_noti = noti.data
                payload: dict = {
                    "type": "new_notification",
                    "data": {
                        "id": new_noti.id,
                        "type": new_noti.type,
                        "is_read": new_noti.is_read,
                        "created_at": new_noti.created_at.isoformat(),
                        "post_id": data.post_id,
                        "actor_id": new_noti.actor.id,
                    }
                }

                await websocket_manager.broadcast(receiver_id, jsonable_encoder(payload))
        return response
    except Exception as e:
        print ("Creating comment error:\n", str(e))
        return raise_error(2009)


@router.delete("/delete-comment/{comment_id}")
async def delete_comment(
        comment_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        post_service=Depends(get_post_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return post_service.delete_comment(db, comment_id, user.get("id"))
    except Exception as e:
        print ("Deleting comment error:\n", str(e))
        return raise_error(2010)
