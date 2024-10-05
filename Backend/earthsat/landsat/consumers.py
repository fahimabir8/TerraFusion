import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f'user_{self.user_id}'
        
        print(f"Adding user {self.user_id} to group {self.group_name}")

        # Debugging: Print to confirm connection
        print(f"WebSocket connection established for user {self.user_id}")

        # Join the user's notification group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Debugging: Print to confirm disconnection
        print(f"WebSocket disconnected for user {self.user_id}")

        # Leave the user's notification group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        # Send the notification to the WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
