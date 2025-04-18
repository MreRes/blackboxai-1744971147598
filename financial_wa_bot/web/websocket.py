from typing import Dict, Set, Any
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        # Store active connections by user_id
        self.active_connections: Dict[int, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        """Connect a new WebSocket client"""
        try:
            await websocket.accept()
            if user_id not in self.active_connections:
                self.active_connections[user_id] = set()
            self.active_connections[user_id].add(websocket)
            logger.info(f"New WebSocket connection for user {user_id}")
        except Exception as e:
            logger.error(f"Error connecting WebSocket: {e}")
            raise

    def disconnect(self, websocket: WebSocket, user_id: int):
        """Disconnect a WebSocket client"""
        try:
            if user_id in self.active_connections:
                self.active_connections[user_id].remove(websocket)
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
            logger.info(f"WebSocket disconnected for user {user_id}")
        except Exception as e:
            logger.error(f"Error disconnecting WebSocket: {e}")

    async def send_personal_message(self, message: Any, websocket: WebSocket):
        """Send a message to a specific client"""
        try:
            if isinstance(message, (dict, list)):
                message = json.dumps(message)
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            raise

    async def broadcast_to_user(self, user_id: int, message: Any):
        """Broadcast a message to all connections of a specific user"""
        if user_id in self.active_connections:
            try:
                if isinstance(message, (dict, list)):
                    message = json.dumps(message)
                for connection in self.active_connections[user_id]:
                    try:
                        await connection.send_text(message)
                    except Exception as e:
                        logger.error(f"Error sending to connection: {e}")
                        # Remove failed connection
                        self.disconnect(connection, user_id)
            except Exception as e:
                logger.error(f"Error broadcasting to user {user_id}: {e}")

    async def broadcast_update(self, user_id: int, update_type: str, data: Any):
        """Broadcast a typed update to a user's connections"""
        try:
            message = {
                "type": update_type,
                "data": data
            }
            await self.broadcast_to_user(user_id, message)
        except Exception as e:
            logger.error(f"Error broadcasting update: {e}")

    async def notify_transaction(self, user_id: int, transaction_data: Dict[str, Any]):
        """Notify about new transaction"""
        await self.broadcast_update(user_id, "transaction", transaction_data)

    async def notify_budget_update(self, user_id: int, budget_data: Dict[str, Any]):
        """Notify about budget updates"""
        await self.broadcast_update(user_id, "budget", budget_data)

    async def notify_balance_update(self, user_id: int, balance_data: Dict[str, Any]):
        """Notify about balance changes"""
        await self.broadcast_update(user_id, "balance", balance_data)

    async def notify_notification(self, user_id: int, notification_data: Dict[str, Any]):
        """Notify about new notifications"""
        await self.broadcast_update(user_id, "notification", notification_data)
