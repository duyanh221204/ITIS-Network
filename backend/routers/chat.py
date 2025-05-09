from fastapi import APIRouter, WebSocket, Query, Depends, status
from fastapi.encoders import jsonable_encoder

from schemas.chat import ConversationCreateSchema, MessageCreateSchema
from services.chat_service import get_chat_service
from utils.configs.authentication import get_current_user
from utils.configs.database import get_db
from utils.configs.websocket import websocket_manager, can_connect
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
        return chat_service.get_or_create_conversation(db, user.get("id"), data.user_id)
    except Exception as e:
        print ("Getting or creating conversation error:\n" + str(e))
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
        return chat_service.get_all_conversations(db, user.get("id"))
    except Exception as e:
        print ("Getting all conversations error:\n" + str(e))
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
        return chat_service.get_all_messages(db, conversation_id, user.get("id"))
    except Exception as e:
        print ("Getting messages error:\n" + str(e))
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

        response = chat_service.send_message(db, conversation_id, user.get("id"), data)
        if response.status == "ok":
            msg = response.data
            payload: dict = {
                "type": "chat_message",
                "data": {
                    "id": msg.id,
                    "content": msg.content,
                    "created_at": msg.created_at.isoformat(),
                    "sender_id": msg.sender.id,
                    "conversation_id": conversation_id
                }
            }

            await websocket_manager.broadcast(conversation_id, jsonable_encoder(payload))
        return response
    except Exception as e:
        print ("Sending message error:\n" + str(e))
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

        response = chat_service.mark_as_read(db, conversation_id, user.get("id"))
        if response.status == "ok":
            payload: dict = {
                "type": "read_receipt",
                "data": {
                    "conversation_id": conversation_id,
                    "reader_id": user.get("id")
                }
            }

            await websocket_manager.broadcast(conversation_id, jsonable_encoder(payload))
        return response
    except Exception as e:
        print ("Marking messages as read error:\n", str(e))
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
        return chat_service.unread_count(db, user.get("id"))
    except Exception as e:
        print ("Getting unread conversations error:\n", str(e))
        return raise_error(4005)


@router.websocket("/ws/{conversation_id}")
async def chat_websocket(
        conversation_id: int,
        websocket: WebSocket,
        token: str = Query(...),
):
    await websocket.accept()

    user_id = can_connect(token)
    if user_id is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    websocket_manager.connect(conversation_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        print ("Websocket exception:\n", str(e))
    finally:
        websocket_manager.disconnect(conversation_id, websocket)
