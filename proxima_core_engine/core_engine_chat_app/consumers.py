import json
from channels.db import database_sync_to_async
import asyncio
import base64
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
from chat.serializers import NestedTripSerializer, TripSerializer, ChatSerializer, NestedChatSerializer  # new
from chat.models import Trip, Chat  # new
from core_engine_community_app.models import Community, Comment
from core_engine_tenant_users_app.models import Client

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        await super().disconnect(code)

    #  Responsible for processing all messages that come to the server
    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'chat.message':
            await self.send_json({
                'type': message_type,
                'data': "This is a new custom message to test",#content.get('data'),
            })


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


class StreamAudioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        audio_data = text_data_json['audio']

        # Send audio data to the client
        await self.send(json.dumps({
            'audio': audio_data
        }))


class StreamAudioSaveConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.file = open("audio.wav", "wb")
        await self.accept()

    async def disconnect(self, close_code):
        self.file.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        audio_data = text_data_json['audio']
        decoded_data = base64.b64decode(audio_data)

        # Save audio data to file
        self.file.write(decoded_data)

        # Send acknowledgment back to the client
        await self.send(json.dumps({
            'status': 'received'
        }))


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



class TaxiConsumer(AsyncJsonWebsocketConsumer):
    groups = ['test']

    # new
    @database_sync_to_async
    def _create_trip(self, data):
        serializer = TripSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.create(serializer.validated_data)

    # new
    @database_sync_to_async
    def _get_trip_data(self, trip):
        return NestedTripSerializer(trip).data

    @database_sync_to_async
    def _get_user_group(self, user):
        return user.groups.first().name


    @database_sync_to_async
    def _get_trip_ids(self, user):
        user_groups = user.groups.values_list('name', flat=True)
        if 'driver' in user_groups:
            trip_ids = user.trips_as_driver.exclude(
                status=Trip.COMPLETED
            ).only('id').values_list('id', flat=True)
        else:
            trip_ids = user.trips_as_rider.exclude(
                status=Trip.COMPLETED
            ).only('id').values_list('id', flat=True)
        return map(str, trip_ids)

    async def connect(self):
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
        else:
            user_group = await self._get_user_group(user)
            if user_group == 'driver':
                await self.channel_layer.group_add(
                    group='drivers',
                    channel=self.channel_name
                )

            # new
            for trip_id in await self._get_trip_ids(user):
                await self.channel_layer.group_add(
                    group=trip_id,
                    channel=self.channel_name
                )

            await self.accept()

    # new
    async def create_trip(self, message):
        data = message.get('data')
        trip = await self._create_trip(data)
        trip_data = await self._get_trip_data(trip)

        await self.send_json({
          'type': 'echo.message',
          'data': trip_data,
        })

    async def disconnect(self, code):
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
        else:
            user_group = await self._get_user_group(user)
            if user_group == 'driver':
                await self.channel_layer.group_discard(
                    group='drivers',
                    channel=self.channel_name
                )

            # new
            for trip_id in await self._get_trip_ids(user):
                await self.channel_layer.group_discard(
                    group=trip_id,
                    channel=self.channel_name
                )

        await super().disconnect(code)

    # changed
    async def echo_message(self, message):
        await self.send_json(message)

    # changed
    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'create.trip':
            await self.create_trip(content)
        elif message_type == 'echo.message':
            await self.echo_message(content)
        elif message_type == 'update.trip': # new
            await self.update_trip(content)

    async def create_trip(self, message):
        data = message.get('data')
        trip = await self._create_trip(data)
        trip_data = await self._get_trip_data(trip)

        # Send rider requests to all drivers.
        await self.channel_layer.group_send(group='drivers', message={
            'type': 'echo.message',
            'data': trip_data
        })

        # Add rider to trip group.
        await self.channel_layer.group_add( # new
            group=f'{trip.id}',
            channel=self.channel_name
        )

        await self.send_json({
            'type': 'echo.message',
            'data': trip_data,
        })

    # new
    async def update_trip(self, message):
        data = message.get('data')
        trip = await self._update_trip(data)
        trip_id = f'{trip.id}'
        trip_data = await self._get_trip_data(trip)

        # Send update to rider.
        await self.channel_layer.group_send(
            group=trip_id,
            message={
                'type': 'echo.message',
                'data': trip_data,
            }
        )

        # Add driver to the trip group.
        await self.channel_layer.group_add(
            group=trip_id,
            channel=self.channel_name
        )

        await self.send_json({
            'type': 'echo.message',
            'data': trip_data
        })

    # new
    @database_sync_to_async
    def _update_trip(self, data):
        instance = Trip.objects.get(id=data.get('id'))
        serializer = TripSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.update(instance, serializer.validated_data)

