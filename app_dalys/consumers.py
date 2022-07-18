import json
import os
from balena import Balena
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, SyncConsumer, WebsocketConsumer, JsonWebsocketConsumer
from .models import Node_Power
from channels.layers import get_channel_layer

class DalysConsumer(AsyncWebsocketConsumer):
    # SET VARIABLES
    group_name = 'dalys'
    channel_name = ''

    async def connect(self):
        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        json_data = json.loads(text_data)        
        # Send message to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'stream.message',
                'message': json_data
            }
        )
        # Send history to group               
        if json_data['Action'] == 'Heartbeat':
            # GET NODE DETAILS
            node_id = json_data['Node_ID']
            # get history data
            json_history_data = await get_data.get_history_data(Node_Power, node_id)
            # GET SEND DATA
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'stream.message',
                    'message': json_history_data
                }
        )

    # Receive message from room group
    async def stream_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

class get_data:
    # get history data
    async def get_history_data(object, node_id):
        json_history_data = {}
        try:            
            json_history_data['Data'] = await json.loads(object.objects.filter(Node = node_id).order_by('-id')[:1440].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('10Min').mean().fillna(method='backfill').tail(140).to_json(orient="table"))
            json_history_data['Data_Type'] = await "History_Data"
            json_history_data['Node_ID'] = await node_id            
        except Exception as e:
            print('{!r}; Get History data failed - '.format(e))
        return json_history_data