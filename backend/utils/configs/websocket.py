from fastapi import WebSocket
from jose import jwt

from utils.configs.authentication import SECRET_KEY, ALGORITHM


class ConnectionManager:
    def __init__(self):
        self.active: dict[int, list[WebSocket]] = {}

    def connect(self, key: int, websocket: WebSocket):
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


def can_connect(token: str) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            return None
    except Exception as e:
        print ("Validating user error:\n", str(e))
        return None

    return int(user_id)
