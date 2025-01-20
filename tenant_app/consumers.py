# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = f'user_{self.user.id}'

        if self.user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            logger.info(f"User {self.user.username} connected to WebSocket and joined group {self.group_name}")

    async def disconnect(self, close_code):
        logger.info(f"User {self.user.username} disconnected from WebSocket")
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        message = event['message']
        logger.info(f"Processing notification for {self.user.username}: {message}")
        await self.send(text_data=json.dumps({
            'message': message
        }))
        logger.info(f"Message sent to {self.user.username} through WebSocket")