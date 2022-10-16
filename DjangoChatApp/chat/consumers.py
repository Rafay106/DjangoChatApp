from channels.generic.websocket import AsyncWebsocketConsumer
from time import sleep
import asyncio
import json

class MyWSC(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connection accepted")
        print("Self: ", self.groups)
        await self.accept()
        await self.send(text_data=json.dumps({
            'type' : 'connection_estabilished',
            'message' : 'You are now connected!'
        }))

    async def receive(self, text_data):
        msg_data_json = json.loads(text_data)
        message = msg_data_json['message']
        print("Message from client: ", message)

        await self.send(text_data = json.dumps({
            'type' : 'chat',
            'message' : message
        }))
        

    async def disconnect(self, code):
        pass
