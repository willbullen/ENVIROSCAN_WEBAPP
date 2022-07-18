import json
import os
from balena import Balena
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, SyncConsumer, WebsocketConsumer, JsonWebsocketConsumer
from .models import Node_Power
from channels.layers import get_channel_layer

class DalysConsumer(WebsocketConsumer):
    # SET VARIABLES
    group_name = 'dalys'
    channel_name = ''

    def async_send(self, channel_name, jsonData):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': jsonData})

    def connect(self):
        # JOIN GROUP
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        json_data = json.loads(text_data)
        if json_data['Action'] == 'Heartbeat':
            # tag history onto data
            json_data['History'] = Get_Data.get_history_data(Node_Power, json_data['Node_ID'])
            # send it
            self.async_send(self.group_name, json_data)

    def stream_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))

class Get_Data:

    def get_history_data(object, node_id):
        history = {}
        try:            
            history = json.loads(object.objects.filter(Node = node_id).order_by('-id')[:1440].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('10Min').mean().fillna(method='backfill').tail(140).to_json(orient="table"))          
        except Exception as e:
            print('{!r}; Get History data failed - '.format(e))
        return history