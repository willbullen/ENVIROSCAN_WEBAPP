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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'message',
                'message': message
            }
        )
        # Send history to group
        jsonData = json.loads(text_data)        
        if jsonData['Action'] == 'Heartbeat':
            # GET NODE DETAILS
            Node_ID = jsonData['Node_ID']
            # GET SEND DATA
            self.async_send(self.group_name, Get_Data.get_History_Data(Node_Power, Node_ID))
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'message',
                    'message': Get_Data.get_History_Data(Node_Power, Node_ID)
                }
        )

    # Receive message from room group
    async def stream_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

class Get_Data:

    def get_History_Data(object, node_id):
        Ground_Station = {}
        try:            
            Ground_Station['Data'] = json.loads(object.objects.filter(Node = node_id).order_by('-id')[:1440].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('10Min').mean().fillna(method='backfill').tail(140).to_json(orient="table"))
            Ground_Station['Data_Type'] = "History_Data"
            Ground_Station['Node_ID'] = node_id            
        except Exception as e:
            print('{!r}; Get History data failed - '.format(e))
        return Ground_Station