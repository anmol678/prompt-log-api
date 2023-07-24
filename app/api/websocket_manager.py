from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    async def disconnect(self, client_id: str):
        await self.active_connections[client_id].close()
        del self.active_connections[client_id]

    async def send_message(self, client_id: str, message: str):
        await self.active_connections[client_id].send_text(message)

manager = ConnectionManager()
