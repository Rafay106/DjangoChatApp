from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from .models import *
import json

from datetime import date, datetime


class MyWSC(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connection accepted")
        self.groupName = self.scope["url_route"]["kwargs"]["groupName"]

        await self.channel_layer.group_add(self.groupName, self.channel_name)
        await self.accept()
        await self.send(
            text_data=json.dumps(
                {"type": "connection_estabilished", "message": "You are now connected!"}
            )
        )

    async def receive(self, text_data):
        message = json.loads(text_data)["message"]

        if self.scope["user"].is_authenticated:
            groupId = self.groupName.split("-")[0]
            room = await database_sync_to_async(get_object_or_404)(
                RoomModel, id=groupId
            )
            user = await database_sync_to_async(UserModel.objects.get)(
                email=self.scope["user"]
            )

            chat = MessageModel(user=user, room=room, body=message)
            await database_sync_to_async(chat.save)()
            await database_sync_to_async(room.participants.add)(user)

            userData = {
                "msg": message,
                "username": user.username,
                "avatar_url": user.avatar.url,
                "msg_age": chat.created.isoformat(),
            }

            await self.channel_layer.group_send(
                self.groupName, {"type": "chat.content", "user": userData}
            )
        else:
            await self.send(
                {
                    "type": "websocket.send",
                    "user": json.dumps(
                        {"msg": "Login Required", "username": "Anonymous"}
                    ),
                }
            )

    async def chat_content(self, event):
        await self.send(json.dumps({"type": "websocket.send", "user": event["user"]}))

    async def disconnect(self, code):
        print("Connection disconnected")
