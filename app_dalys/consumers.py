import json
import os
from balena import Balena
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, SyncConsumer, WebsocketConsumer, JsonWebsocketConsumer
from data.models import Picarro_Data, Nodes
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
        pass

    def receive(self, text_data):
        jsonData = json.loads(text_data)        
        if jsonData['Action'] == 'Heartbeat':
            # GET NODE DETAILS
            Node_ID = jsonData['Node_ID']
            # GET SEND DATA
            #self.async_send(self.group_name, Get_Data.get_History_Data(Picarro_Data, Node_ID))

    def stream_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))

class Get_Data:

    def get_History_Data(object, node_id):
        Ground_Station = {}
        try:            
            Ground_Station['Data'] = json.loads(object.objects.filter(Node_ID = node_id).order_by('-id')[:1440].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('10Min').mean().fillna(method='backfill').tail(140).to_json(orient="table"))
            Ground_Station['Data_Type'] = "History_Data"
            Ground_Station['Node_ID'] = node_id            
        except Exception as e:
            print('{!r}; Get History data failed - '.format(e))
        return Ground_Station