from fastapi import APIRouter, WebSocket, Query, Depends, status
from fastapi.encoders import jsonable_encoder

from schemas.authentication import TokenDataSchema
from schemas.chat import ConversationCreateSchema, MessageCreateSchema
from services.chat_service import get_chat_service, ChatService
from configs.authentication import get_current_user
from configs.websocket import websocket_manager, can_connect
from utils.exceptions import raise_error

router = APIRouter(
    prefix="/api/chats",
    tags=["Chat"]
)


@router.post("/conversation")
async def get_or_create_conversation(
        data: ConversationCreateSchema,
        user: TokenDataSchema = Depends(get_current_user),
        chat_service: ChatService = Depends(get_chat_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return chat_service.get_or_create_conversation(user.id, data.user_id)
    except Exception as e:
        print ("Retrieving or creating conversation error:\n" + str(e))
        return raise_error(4000)


@router.get("/conversations")
async def get_all_conversations(
        user: TokenDataSchema = Depends(get_current_user),
        chat_service: ChatService = Depends(get_chat_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return chat_service.get_all_conversations(user.id)
    except Exception as e:
        print ("Retrieving all conversations error:\n" + str(e))
        return raise_error(4001)


@router.get("/conversation/{conversation_id}/messages")
async def get_all_messages(
        conversation_id: int,
        user: TokenDataSchema = Depends(get_current_user),
        chat_service: ChatService = Depends(get_chat_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return chat_service.get_all_messages(conversation_id, user.id)
    except Exception as e:
        print ("Retrieving messages error:\n" + str(e))
        return raise_error(4002)


@router.post("/conversations/{conversation_id}/message")
async def send_message(
        data: MessageCreateSchema,
        conversation_id: int,
        user: TokenDataSchema = Depends(get_current_user),
        chat_service: ChatService = Depends(get_chat_service)
):
    try:
        if user is None:
            return raise_error(1005)

        response = chat_service.send_message(conversation_id, user.id, data)
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
        user: TokenDataSchema = Depends(get_current_user),
        chat_service: ChatService = Depends(get_chat_service)
):
    try:
        if user is None:
            return raise_error(1005)

        response = chat_service.mark_as_read(conversation_id, user.id)
        if response.status == "ok":
            payload: dict = {
                "type": "read_receipt",
                "data": {
                    "conversation_id": conversation_id,
                    "reader_id": user.id
                }
            }

            await websocket_manager.broadcast(conversation_id, jsonable_encoder(payload))
        return response
    except Exception as e:
        print ("Marking messages as read error:\n" + str(e))
        return raise_error(4004)


@router.get("/conversations/unread")
async def unread_count(
        user: TokenDataSchema = Depends(get_current_user),
        chat_service: ChatService = Depends(get_chat_service)
):
    try:
        if user is None:
            return raise_error(1005)
        return chat_service.unread_count(user.id)
    except Exception as e:
        print ("Retrieving unread conversations error:\n" + str(e))
        return raise_error(4005)


@router.websocket("/ws/{conversation_id}")
async def chat_websocket(
        conversation_id: int,
        websocket: WebSocket,
        token: str = Query(...),
):
    await websocket.accept()

    user = can_connect(token)
    if user is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    websocket_manager.connect(conversation_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        print ("Websocket exception:\n" + str(e))
    finally:
        websocket_manager.disconnect(conversation_id, websocket)
