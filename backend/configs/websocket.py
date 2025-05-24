from fastapi import WebSocket, Depends, Query, WebSocketException, status

from repositories.invalidated_token_repository import get_invalidated_token_repository, InvalidatedTokenRepository
from schemas.authentication import TokenDataSchema
from configs.authentication import verify_token


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


def can_connect(
        token: str = Query(...),
        invalidated_token_repository: InvalidatedTokenRepository = Depends(get_invalidated_token_repository)
) -> TokenDataSchema | WebSocketException:
    user = verify_token(token, invalidated_token_repository)

    if user is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return user
