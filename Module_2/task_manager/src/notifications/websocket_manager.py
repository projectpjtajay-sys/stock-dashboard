import logging
from fastapi import WebSocket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class WebSocketManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        # Disconnect and close any old socket for the same user
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].close()
                logger.info(f"Closed previous WebSocket for user {user_id}")
            except Exception as e:
                logger.warning(f"Error closing old connection for user {user_id}: {e}")

        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"User {user_id} connected via WebSocket.")

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"User {user_id} disconnected from WebSocket.")

    async def send_personal_message(self, user_id: int, message: str):
        websocket = self.active_connections.get(user_id)
        if websocket:
            try:
                await websocket.send_text(message)
                logger.info(f"Sent to User {user_id}: {message}")
            except Exception as e:
                logger.error(f"Failed to send to user {user_id}: {e}")
                self.disconnect(user_id)

    async def broadcast(self, message: str):
        for user_id, websocket in list(self.active_connections.items()):
            try:
                await websocket.send_text(message)
                logger.info(f"Broadcast to User {user_id}")
            except Exception as e:
                logger.error(f"Broadcast failed for user {user_id}: {e}")
                self.disconnect(user_id)

manager = WebSocketManager()
