from datetime import datetime
from types import SimpleNamespace

from fastapi import APIRouter, WebSocket, Query, Depends

from schemas.chat import ConversationCreateSchema, MessageCreateSchema
from services.chat_service import get_chat_service
from utils.configs.authentication import get_current_user
from utils.configs.database import SessionLocal, get_db
from utils.configs.websocket import websocket_manager, get_sender
from utils.exceptions import raise_error

router = APIRouter(
    prefix="/api/chats",
    tags=["Chat"]
)


@router.post("/conversation")
async def get_or_create_conversation(
        data: ConversationCreateSchema,
        db=Depends(get_db),
        user=Depends(get_current_user),
        chat_service=Depends(get_chat_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return chat_service.get_or_create_conversation(db, user["id"], data.user_id)
    except Exception:
        return raise_error(4000)


@router.get("/conversations")
async def get_all_conversations(
        db=Depends(get_db),
        user=Depends(get_current_user),
        chat_service=Depends(get_chat_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return chat_service.get_all_conversations(db, user["id"])
    except Exception:
        return raise_error(4001)


@router.get("/conversation/{conversation_id}/messages")
async def get_all_messages(
        conversation_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        chat_service=Depends(get_chat_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return chat_service.get_all_messages(db, conversation_id, user["id"])
    except Exception:
        return raise_error(4002)


@router.post("/conversations/{conversation_id}/message")
async def send_message(
        data: MessageCreateSchema,
        conversation_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        chat_service=Depends(get_chat_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return chat_service.send_message(db, conversation_id, user["id"], data)
    except Exception:
        return raise_error(4003)


@router.put("/conversations/{conversation_id}/read")
async def mark_as_read(
        conversation_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        chat_service=Depends(get_chat_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return chat_service.mark_as_read(db, conversation_id, user["id"])
    except Exception:
        return raise_error(4004)


@router.get("/conversations/unread")
async def unread_count(
        db=Depends(get_db),
        user=Depends(get_current_user),
        chat_service=Depends(get_chat_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return chat_service.unread_count(db, user["id"])
    except Exception:
        return raise_error(4005)


@router.websocket("/ws/{conversation_id}")
async def chat_websocket(
        conversation_id: int,
        websocket: WebSocket,
        token: str = Query(...),
        chat_service=Depends(get_chat_service)
):
    user_id = get_sender(token, websocket)
    if user_id is None:
        return

    await websocket_manager.connect(conversation_id, websocket)
    db = SessionLocal()
    try:
        while True:
            data = await websocket.receive_text()
            response = chat_service.send_message(db, conversation_id, user_id, SimpleNamespace(content=data))

            if response.status == "ok":
                await websocket_manager.broadcast(
                    conversation_id,
                    {
                        "id": response.data.id,
                        "content": data,
                        "created_at": str(datetime.now()),
                        "sender_id": user_id
                    }
                )
    except Exception:
        websocket_manager.disconnect(conversation_id, websocket)
    finally:
        db.close()
