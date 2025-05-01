from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active: dict[int, list[WebSocket]] = {}

    async def connect(self, conversation_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active.setdefault(conversation_id, []).append(websocket)

    def disconnect(self, conversation_id: int, websocket: WebSocket):
        connections = self.active.get(conversation_id, [])
        if websocket in connections:
            connections.remove(websocket)

            if not connections:
                self.active.pop(conversation_id, None)

    async def broadcast(self, conversation_id: int, message: dict):
        for ws in self.active.get(conversation_id, []):
            await ws.send_json(message)


websocket_manager = ConnectionManager()
