import asyncio

from fastapi import WebSocket, status
from jose import jwt

from utils.configs.authentication import SECRET_KEY, ALGORITHM


class ConnectionManager:
    def __init__(self):
        self.active: dict[int, list[WebSocket]] = {}
        self.loop: asyncio.AbstractEventLoop | None = None

    async def connect(self, key: int, websocket: WebSocket):
        await websocket.accept()
        self.active.setdefault(key, []).append(websocket)

    def disconnect(self, key: int, websocket: WebSocket):
        connections = self.active.get(key, [])
        if websocket in connections:
            connections.remove(websocket)

            if not connections:
                self.active.pop(key, None)

    async def broadcast(self, key: int, message: dict):
        for ws in self.active.get(key, []):
            await ws.send_json(message)


websocket_manager = ConnectionManager()


async def get_sender(token: str, websocket: WebSocket) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if user_id is None or username is None:
            return await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    except Exception:
        return await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    return user_id
