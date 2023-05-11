import json
from channels.db import database_sync_to_async
import asyncio
import base64
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
from core_engine_community_app.models import Community, Comment
from core_engine_tenant_users_app.models import Client


class CommunityConsumer(AsyncJsonWebsocketConsumer):
    groups = ['testcommunity']

    async def connect(self): # changed
        await self.channel_layer.group_add(
            group='testcommunity',
            channel=self.channel_name
        )
        await self.accept()

    async def disconnect(self, code): # changed
        await self.channel_layer.group_discard(
            group='testcommunity',
            channel=self.channel_name
        )
        await super().disconnect(code)

    async def community_message(self, message):
        await self.send_json({
            'type': message.get('type'),
            'data': message.get('data'),
        })

    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'community.message':
            await self.send_json({
                'type': message_type,
                'data': content.get('data'),
            })




class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.community_id = str(self.scope["url_route"]["kwargs"]["uuid"])
        self.group = await database_sync_to_async(Community.objects.get)(uuid = self.group_uuid)
        await self.channel_layer.group_add(
                self.community_id,self.channel_name)
   
        self.client = self.scope["client"]
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        type = text_data.get("type", None)
        client = text_data.get("client", None)
        message = text_data.get("message", None)
        author = text_data.get("author", None)
        if type == "community_message":
            client = await database_sync_to_async(Client.objects.get)(client=client)
            comment= await database_sync_to_async(Comment.objects.create)(
            client = client,
            comment = comment,
            community =self.community
            )
        await self.channel_layer.community_send(self.community_id, {
            "type":"community_message",
            "comment":str(comment),
            "client":client
        })

    async def text_message(self, event):
        comment = event["comment"]
        client = event.get("client")
        
        returned_data = {
            "type":"community_message",
            "comment":comment,
            "community_id":self.community_id
        }
        await self.send(json.dumps(
                returned_data
                ))



