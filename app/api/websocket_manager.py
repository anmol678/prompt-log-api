from fastapi import WebSocket
from app.sqlite.schemas import Log


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.new_logs: list[Log] = []

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    async def disconnect(self, client_id: str):
        await self.active_connections[client_id].close()
        del self.active_connections[client_id]

    async def send_message(self, client_id: str, message: str):
        await self.active_connections[client_id].send_text(message)
    
    def add_log(self, log: Log):
        self.new_logs.append(log)

    async def send_notification(self):
        self.new_logs.pop()
        for client_id in self.active_connections.keys():
            await self.send_message(client_id, "new logs")


manager = ConnectionManager()
