import json
import os
from balena import Balena
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, SyncConsumer, WebsocketConsumer, JsonWebsocketConsumer
from data.models import UPS, Generator, Autosonde_Ground_Station, Aethalometer_Data, Picarro_Data, Picarro_Alarms, Picarro_Logs, Picarro_Properties, Picarro_PM, Picarro_Jobs, Tucson_Data, SOX_Data, NOX_Data, Baloon_Data, Nodes, Node_Type, Autosonde_Soundings, Autosonde_Sounding_Data, Autosonde_Logs
import datetime
from django.core import serializers
from channels.layers import get_channel_layer

class StatusConsumer(WebsocketConsumer):

    group_name = 'status'

    def async_send(self, channel_name, jsonData):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': jsonData})

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        jsonData = json.loads(text_data)

    def background_task(self):
        print('')

class HomeConsumer(WebsocketConsumer):
    # SET VARIABLES
    db_name = 'UPS'
    group_name = 'ups'
    channel_name = ''

    def async_send(self, channel_name, jsonData):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': jsonData})

    def connect(self):
        # JOIN ROOM GROUP
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
            # GET NODE ID
            Node_ID = jsonData['Node_ID']
            # SET NODE STATUS
            NodeStatus = 0
            NodeStatusDescription = ''
            balena = Balena()                    
            try:
                balenaCredentials = {'username':'gh_willbullen', 'password':'B@ff1ed!2020'}
                balena.auth.login(**balenaCredentials)
                nodeData = balena.models.device.get(Nodes.objects.only('Node_Device_ID').get(id = Node_ID).Node_Device_ID)
                if nodeData['api_heartbeat_state'] == 'Offline':
                    NodeStatus = 1
                    NodeStatusDescription = 'Node currently offline.'
                else:
                    NodeStatus = 0
                    NodeStatusDescription = 'Node online.'
            except Exception as e:
                print('{!r}; Get node status failed - '.format(e))                    
            
            try:
                Nodes.objects.filter(id=Node_ID).update(Node_Status = NodeStatus, Node_Status_Description = NodeStatusDescription)
            except Exception as e:
                print('{!r}; Save status failed - '.format(e))                    
            
            #self.async_send(self.group_name, Get_Data.get_History_Data(Generator, Node_ID))
            #self.async_send(self.group_name, Get_Data.get_Current_Data(Generator, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Status_Data(Nodes, Node_ID))

class GeneratorConsumer(WebsocketConsumer):
    # SET VARIABLES
    db_name = 'UPS'
    group_name = 'ups'
    channel_name = ''

    def async_send(self, channel_name, jsonData):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': jsonData})

    def connect(self):
        # JOIN ROOM GROUP
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
            # GET NODE ID
            Node_ID = jsonData['Node_ID']
            # SET NODE STATUS
            NodeStatus = 0
            NodeStatusDescription = ''
            balena = Balena()                    
            try:
                balenaCredentials = {'username':'gh_willbullen', 'password':'B@ff1ed!2020'}
                balena.auth.login(**balenaCredentials)
                nodeData = balena.models.device.get(Nodes.objects.only('Node_Device_ID').get(id = Node_ID).Node_Device_ID)
                if nodeData['api_heartbeat_state'] == 'Offline':
                    NodeStatus = 1
                    NodeStatusDescription = 'Node currently offline.'
                else:
                    NodeStatus = 0
                    NodeStatusDescription = 'Node online.'
            except Exception as e:
                print('{!r}; Get node status failed - '.format(e))                    
            
            try:
                Nodes.objects.filter(id=Node_ID).update(Node_Status = NodeStatus, Node_Status_Description = NodeStatusDescription)
            except Exception as e:
                print('{!r}; Save status failed - '.format(e))                    
            
            self.async_send(self.group_name, Get_Data.get_History_Data(Generator, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Current_Data(Generator, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Status_Data(Nodes, Node_ID))

class UPSConsumer(WebsocketConsumer):
    # SET VARIABLES
    db_name = 'UPS'
    group_name = 'ups'
    channel_name = ''

    def async_send(self, channel_name, jsonData):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': jsonData})

    def connect(self):
        # JOIN ROOM GROUP
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
            # GET NODE ID
            Node_ID = jsonData['Node_ID']
            # SET NODE STATUS
            NodeStatus = 0
            NodeStatusDescription = ''
            balena = Balena()                    
            try:
                balenaCredentials = {'username':'gh_willbullen', 'password':'B@ff1ed!2020'}
                balena.auth.login(**balenaCredentials)
                nodeData = balena.models.device.get(Nodes.objects.only('Node_Device_ID').get(id = Node_ID).Node_Device_ID)
                if nodeData['api_heartbeat_state'] == 'Offline':
                    NodeStatus = 1
                    NodeStatusDescription = 'Node currently offline.'
                else:
                    NodeStatus = 0
                    NodeStatusDescription = 'Node online.'
            except Exception as e:
                print('{!r}; Get node status failed - '.format(e))                    
            
            try:
                Nodes.objects.filter(id=Node_ID).update(Node_Status = NodeStatus, Node_Status_Description = NodeStatusDescription)
            except Exception as e:
                print('{!r}; Save status failed - '.format(e))                    
            
            self.async_send(self.group_name, Get_Data.get_History_Data(UPS, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Current_Data(UPS, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Status_Data(Nodes, Node_ID))

class AethalometerConsumer(WebsocketConsumer):
    # SET VARIABLES
    db_name = 'Athalometer_AE33'
    group_name = 'athalometer'
    channel_name = ''

    def async_send(self, channel_name, jsonData):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': jsonData})

    def connect(self):
        # JOIN ROOM GROUP
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
            # GET NODE ID
            Node_ID = jsonData['Node_ID']
            # SET NODE STATUS
            NodeStatus = 0
            NodeStatusDescription = ''
            balena = Balena()                    
            try:
                balenaCredentials = {'username':'gh_willbullen', 'password':'B@ff1ed!2020'}
                balena.auth.login(**balenaCredentials)
                nodeData = balena.models.device.get(Nodes.objects.only('Node_Device_ID').get(id = Node_ID).Node_Device_ID)
                if nodeData['api_heartbeat_state'] == 'Offline':
                    NodeStatus = 1
                    NodeStatusDescription = 'Node currently offline.'
                else:
                    NodeStatus = 0
                    NodeStatusDescription = 'Node online.'
            except Exception as e:
                print('{!r}; Get node status failed - '.format(e))                    
            
            try:
                Nodes.objects.filter(id=Node_ID).update(Node_Status = NodeStatus, Node_Status_Description = NodeStatusDescription)
            except Exception as e:
                print('{!r}; Save status failed - '.format(e))                    
            
            self.async_send(self.group_name, Get_Data.get_History_Data(Aethalometer_Data, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Current_Data(Aethalometer_Data, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Status_Data(Nodes, Node_ID))

    def stream_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))

class PicarroConsumer(WebsocketConsumer):
    # SET VARIABLES
    db_name = 'Picarro G2401'
    group_name = 'picarro'
    channel_name = ''

    def async_send(self, channel_name, jsonData):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': jsonData})

    def connect(self):
        # JOIN ROOM GROUP
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
            # GET NODE ID
            Node_ID = jsonData['Node_ID']
            # SET NODE STATUS
            NodeStatus = 0
            NodeStatusDescription = ''
            balena = Balena()                    
            try:
                balenaCredentials = {'username':'gh_willbullen', 'password':'B@ff1ed!2020'}
                balena.auth.login(**balenaCredentials)
                nodeData = balena.models.device.get(Nodes.objects.only('Node_Device_ID').get(id = Node_ID).Node_Device_ID)
                if nodeData['api_heartbeat_state'] == 'Offline':
                    NodeStatus = 1
                    NodeStatusDescription = 'Node currently offline.'
                else:
                    NodeStatus = 0
                    NodeStatusDescription = 'Node online.'
            except Exception as e:
                print('{!r}; Get node status failed - '.format(e))                    
            
            try:
                Nodes.objects.filter(id=Node_ID).update(Node_Status = NodeStatus, Node_Status_Description = NodeStatusDescription)
            except Exception as e:
                print('{!r}; Save status failed - '.format(e))                    
            
            self.async_send(self.group_name, Get_Data.get_History_Data(Picarro_Data, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Current_Data(Picarro_Data, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Status_Data(Nodes, Node_ID))

    def stream_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))

class TucsonConsumer(WebsocketConsumer):
    # SET VARIABLES
    db_name = 'TUCSON'
    group_name = 'tucson'
    channel_name = ''

    def async_send(self, channel_name, jsonData):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': jsonData})

    def connect(self):
        # JOIN ROOM GROUP
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
            # GET NODE ID
            Node_ID = jsonData['Node_ID']
            # SET NODE STATUS
            NodeStatus = 0
            NodeStatusDescription = ''
            balena = Balena()                    
            try:
                balenaCredentials = {'username':'gh_willbullen', 'password':'B@ff1ed!2020'}
                balena.auth.login(**balenaCredentials)
                nodeData = balena.models.device.get(Nodes.objects.only('Node_Device_ID').get(id = Node_ID).Node_Device_ID)
                if nodeData['api_heartbeat_state'] == 'Offline':
                    NodeStatus = 1
                    NodeStatusDescription = 'Node currently offline.'
                else:
                    NodeStatus = 0
                    NodeStatusDescription = 'Node online.'
            except Exception as e:
                print('{!r}; Get node status failed - '.format(e))                    
            
            try:
                Nodes.objects.filter(id=Node_ID).update(Node_Status = NodeStatus, Node_Status_Description = NodeStatusDescription)
            except Exception as e:
                print('{!r}; Save status failed - '.format(e))                    
            
            self.async_send(self.group_name, Get_Data.get_History_Data(Tucson_Data, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Current_Data(Tucson_Data, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Status_Data(Nodes, Node_ID))

    def stream_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))

class NOXConsumer(WebsocketConsumer):
    # SET VARIABLES
    db_name = 'NOX'
    group_name = 'nox'
    channel_name = ''

    def async_send(self, channel_name, jsonData):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': jsonData})

    def connect(self):
        print('NOX WEBSOCKET CONNECTED.............')
        # JOIN ROOM GROUP
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print('RECEIVING DATA.............')
        jsonData = json.loads(text_data)        
        if jsonData['Action'] == 'Heartbeat':
            # GET NODE ID
            Node_ID = jsonData['Node_ID']
            # SET NODE STATUS
            NodeStatus = 0
            NodeStatusDescription = ''
            balena = Balena()                    
            try:
                balenaCredentials = {'username':'gh_willbullen', 'password':'B@ff1ed!2020'}
                balena.auth.login(**balenaCredentials)
                nodeData = balena.models.device.get(Nodes.objects.only('Node_Device_ID').get(id = Node_ID).Node_Device_ID)
                if nodeData['api_heartbeat_state'] == 'Offline':
                    NodeStatus = 1
                    NodeStatusDescription = 'Node currently offline.'
                else:
                    NodeStatus = 0
                    NodeStatusDescription = 'Node online.'
            except Exception as e:
                print('{!r}; Get node status failed - '.format(e))                    
            
            try:
                Nodes.objects.filter(id=Node_ID).update(Node_Status = NodeStatus, Node_Status_Description = NodeStatusDescription)
            except Exception as e:
                print('{!r}; Save status failed - '.format(e))                    
            
            self.async_send(self.group_name, Get_Data.get_History_Data(NOX_Data, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Current_Data(NOX_Data, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Status_Data(Nodes, Node_ID))

    def stream_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))


class SOXConsumer(WebsocketConsumer):
    # SET VARIABLES
    db_name = 'SOX'
    group_name = 'sox'
    channel_name = ''

    def async_send(self, channel_name, jsonData):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': jsonData})

    def connect(self):
        # JOIN ROOM GROUP
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
            # GET NODE ID
            Node_ID = jsonData['Node_ID']
            # SET NODE STATUS
            NodeStatus = 0
            NodeStatusDescription = ''
            balena = Balena()                    
            try:
                balenaCredentials = {'username':'gh_willbullen', 'password':'B@ff1ed!2020'}
                balena.auth.login(**balenaCredentials)
                nodeData = balena.models.device.get(Nodes.objects.only('Node_Device_ID').get(id = Node_ID).Node_Device_ID)
                if nodeData['api_heartbeat_state'] == 'Offline':
                    NodeStatus = 1
                    NodeStatusDescription = 'Node currently offline.'
                else:
                    NodeStatus = 0
                    NodeStatusDescription = 'Node online.'
            except Exception as e:
                print('{!r}; Get node status failed - '.format(e))                    
            
            try:
                Nodes.objects.filter(id=Node_ID).update(Node_Status = NodeStatus, Node_Status_Description = NodeStatusDescription)
            except Exception as e:
                print('{!r}; Save status failed - '.format(e))                    
            
            self.async_send(self.group_name, Get_Data.get_History_Data(SOX_Data, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Current_Data(SOX_Data, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Status_Data(Nodes, Node_ID))

    def stream_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))

class DAQCConsumer(WebsocketConsumer):
    # SET VARIABLES
    db_name = 'SOX'
    group_name = 'sox'
    channel_name = ''

    def async_send(self, channel_name, jsonData):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': jsonData})

    def connect(self):
        # JOIN ROOM GROUP
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
            # GET NODE ID
            Node_ID = jsonData['Node_ID']
            # SET NODE STATUS
            NodeStatus = 0
            NodeStatusDescription = ''
            balena = Balena()                    
            try:
                balenaCredentials = {'username':'gh_willbullen', 'password':'B@ff1ed!2020'}
                balena.auth.login(**balenaCredentials)
                nodeData = balena.models.device.get(Nodes.objects.only('Node_Device_ID').get(id = Node_ID).Node_Device_ID)
                if nodeData['api_heartbeat_state'] == 'Offline':
                    NodeStatus = 1
                    NodeStatusDescription = 'Node currently offline.'
                else:
                    NodeStatus = 0
                    NodeStatusDescription = 'Node online.'
            except Exception as e:
                print('{!r}; Get node status failed - '.format(e))                    
            
            try:
                Nodes.objects.filter(id=Node_ID).update(Node_Status = NodeStatus, Node_Status_Description = NodeStatusDescription)
            except Exception as e:
                print('{!r}; Save status failed - '.format(e))                    
            
            self.async_send(self.group_name, Get_Data.get_History_Data(SOX_Data, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Current_Data(SOX_Data, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Status_Data(Nodes, Node_ID))

    def stream_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))

class AutosondeConsumer(WebsocketConsumer):
    # SET VARIABLES
    db_name = 'Autosonde AS41'
    group_name = 'autosonde'
    channel_name = ''    

    def async_send(self, channel_name, jsonData):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': jsonData})

    def connect(self):
        # JOIN ROOM GROUP
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        jsonData = json.loads(text_data)
        print(jsonData)
        if jsonData['Action'] == 'Heartbeat':
            # GET NODE ID
            Node_ID = jsonData['Node_ID']
            # GET SOUNDING ID
            Sounding_ID = Autosonde_Soundings.objects.filter(Node_ID = Node_ID).latest('id').id
            # SET NODE STATUS
            NodeStatus = 0
            NodeStatusDescription = ''            
            balena = Balena()
            balenaCredentials = {'username':'gh_willbullen', 'password':'B@ff1ed!2020'}
            try:
                balena.auth.login(**balenaCredentials)
                nodeData = balena.models.device.get(Nodes.objects.only('Node_Device_ID').get(id = Node_ID).Node_Device_ID)
                if nodeData['api_heartbeat_state'] == 'Offline':
                    NodeStatus = 1
                    NodeStatusDescription = 'Node currently offline.'
                else:
                    NodeStatus = 0
                    NodeStatusDescription = 'Node online.'
            except Exception as e:
                print('{!r}; Get node status failed - '.format(e))            
            try:
                Nodes.objects.filter(id=Node_ID).update(Node_Status = NodeStatus, Node_Status_Description = NodeStatusDescription)
            except Exception as e:
                print('{!r}; Save status failed - '.format(e))
            # GET DATA
            self.async_send(self.group_name, Get_Data.get_History_Data(Autosonde_Ground_Station, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Autosonde_Logs(Autosonde_Logs, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Soundings(Autosonde_Soundings, Node_ID, Sounding_ID))
            self.async_send(self.group_name, Get_Data.get_Sounding_Data(Autosonde_Sounding_Data, Node_ID, Sounding_ID))
            self.async_send(self.group_name, Get_Data.get_Status_Data(Nodes, Node_ID))
            self.async_send(self.group_name, Get_Data.get_Setup_Data(Nodes, Node_ID))

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

    def get_Current_Data(object, node_id):
        Current_Data = {}
        try:            
            Current_Data['Data'] = {**json.loads(serializers.serialize("json", [object.objects.filter(Node_ID = node_id).latest('id')]))[0]['fields']}
            Current_Data['Data_Type'] = 'Current_Data'
            Current_Data['Node_ID'] = node_id     
        except Exception as e:
            print('{!r}; Get Current data failed - '.format(e))
        return Current_Data

    def get_Sounding_Data(object, node_id, sounding_id):
        Sounding = {}
        try:            
            Sounding['Data'] = json.loads(object.objects.filter(Sounding_ID = sounding_id).to_dataframe().to_json(orient="table"))
            Sounding['Data_Type'] = 'Sounding_Data'
            Sounding['Node_ID'] = node_id    
            Sounding['Sounding_ID'] = sounding_id          
        except Exception as e:
            print('{!r}; Get Sounding data failed - '.format(e))
        return Sounding

    def get_Soundings(object, node_id, sounding_id):
        Soundings = {}
        try:            
            Soundings['Data'] = {**json.loads(serializers.serialize("json", [object.objects.filter(Node_ID = node_id).latest('id')]))[0]['fields']}
            Soundings['Data_Type'] = 'Soundings_Data'
            Soundings['Node_ID'] = node_id  
            Soundings['Sounding_ID'] = sounding_id           
        except Exception as e:
            print('{!r}; Get Soundings data failed - '.format(e))
        return Soundings

    def get_Autosonde_Logs(object, node_id):
        Logs = {}
        try:
            Logs['Data'] = json.loads(object.objects.filter(Node_ID = node_id).to_dataframe().to_json(orient="table"))
            Logs['Data_Type'] = 'Log_Data'
            Logs['Node_ID'] = node_id            
        except Exception as e:
            print('{!r}; Get Autosonde Logs data failed - '.format(e))
        return Logs

    def get_Status_Data(object, node_id):
        Status = {} 
        try:
            Status['Data'] = json.loads(object.objects.all().to_dataframe().to_json(orient="table"))
            Status['Data_Type'] = "Status_Data"
            Status['Node_ID'] = node_id
        except Exception as e:
            print('{!r}; Get status data failed - '.format(e)) 
        return Status

    def get_Setup_Data(object, node_id):
        Setup = {} 
        try:
            Setup['Data'] = json.loads(object.objects.filter(id = node_id).to_dataframe().to_json(orient="table"))
            Setup['Data_Type'] = "Setup_Data"
            Setup['Node_ID'] = node_id
        except Exception as e:
            print('{!r}; Get setup data failed - '.format(e)) 
        return Setup
