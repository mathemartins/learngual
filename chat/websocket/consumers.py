import uuid

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from chat.models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['session'].get('user_id')
        if user_id is None:
            self.scope['session']['user_id'] = str(uuid.uuid4())
        await self.accept()
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(
            room_name,
            self.channel_name
        )

    async def disconnect(self, close_code):
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_discard(room_name, self.channel_name)

    async def receive(self, text_data):
        received_data = json.loads(text_data)
        print(received_data)
        user_id = self.scope['session']['user_id']
        message_content = received_data.get('message')
        message_read = received_data.get('message_read')

        if message_content:
            room_name = self.scope['url_route']['kwargs']['room_name']

            try:
                room = await sync_to_async(ChatRoom.objects.get)(name=room_name)
            except ObjectDoesNotExist:
                room = await sync_to_async(ChatRoom.objects.create)(name=room_name)

            user, _ = await sync_to_async(User.objects.get_or_create)(username=f"Anonymous-{user_id}")

            # Create the message asynchronously
            new_message = await sync_to_async(Message.objects.create)(
                room=room,
                user=user,
                content=message_content
            )

            # Broadcast the message to everyone in the room
            await self.channel_layer.group_send(
                room_name,
                {
                    'type': 'chat_message',
                    'message': message_content,
                    'user': user.username,
                    'timestamp': str(new_message.timestamp),
                    'message_id': new_message.id
                }
            )

        if message_read:
            # Update the message as read by the user
            message = Message.objects.get(id=message_read)
            message.mark_as_read(self.scope['user'])

    async def chat_message(self, event):
        # Send the received message to the WebSocket
        print(event)
        await self.send(text_data=json.dumps(event))
