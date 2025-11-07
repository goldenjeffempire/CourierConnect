import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.parcels.models import Parcel


class TrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.tracking_number = self.scope['url_route']['kwargs']['tracking_number']
        self.room_group_name = f'tracking_{self.tracking_number}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'tracking_update',
                'message': message
            }
        )

    async def tracking_update(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
