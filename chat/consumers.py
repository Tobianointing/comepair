import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage, Notification
from django.contrib.auth.models import User

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        
        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        thread_obj = await self.get_thread(me, other_user)
        self.thread_obj = thread_obj
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })


    async def websocket_receive(self, event):
        print("receive", event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            print(msg)

            user = self.scope['user']
            other_name = self.scope['url_route']['kwargs']['username']
            other = await self.get_other_user(other_name)

            username = 'default'
            if user.is_authenticated:
                username = user.username
            myResponse = {
                 'message': msg,
                'username': username
            }
            
            await self.create_chat_message(user, msg)
            await self.create_notification(other, msg)
         
            
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text": json.dumps(myResponse)
                }
            )

    async def chat_message(self, event):

        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        print("disconnect", event)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]


    @database_sync_to_async
    def create_chat_message(self, me,  msg):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg)

    @database_sync_to_async
    def create_notification(self, other_user, msg):
        last_chat = ChatMessage.objects.latest('id')
        created_notification = Notification.objects.create(notification_user=other_user, notification_chat=last_chat)
        return created_notification
    
    @database_sync_to_async
    def get_other_user(self, other_username):
        return User.objects.get(username=other_username)
