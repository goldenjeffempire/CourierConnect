
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .chat_service import AIChatService
import json


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for real-time AI chat support
    """
    
    async def connect(self):
        self.room_name = f"chat_{self.scope['user'].id if self.scope['user'].is_authenticated else 'guest'}"
        self.room_group_name = f"chat_group_{self.room_name}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send welcome message
        await self.send_json({
            'type': 'chat_message',
            'message': 'Welcome to Courier Core support! How can I help you today?',
            'sender': 'bot',
            'timestamp': self.get_timestamp()
        })
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive_json(self, content):
        message = content.get('message', '')
        
        if not message:
            return
        
        # Echo user message
        await self.send_json({
            'type': 'chat_message',
            'message': message,
            'sender': 'user',
            'timestamp': self.get_timestamp()
        })
        
        # Get AI response
        response = await self.get_ai_response(message)
        
        # Send AI response
        await self.send_json({
            'type': 'chat_message',
            'message': response,
            'sender': 'bot',
            'timestamp': self.get_timestamp()
        })
    
    @database_sync_to_async
    def get_ai_response(self, message):
        chat_service = AIChatService()
        return chat_service.get_response(message)
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()
