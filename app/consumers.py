import json
import os
from balena import Balena
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, SyncConsumer, WebsocketConsumer, JsonWebsocketConsumer
from data.models import Picarro_Data, Picarro_Alarms, Picarro_Logs, Picarro_Properties, Picarro_PM, Picarro_Jobs, SOX_Data, NOX_Data, Baloon_Data, Nodes, Node_Type
import time
from time import sleep
from datetime import datetime, timezone
from django.core import serializers
from channels.layers import get_channel_layer

class PicarroConsumer(WebsocketConsumer):

    datetime_check_picarro = ''
    db_name = 'Picarro G2401'
    group_name = 'picarro'
    channel_name = ''
    balenaCredentials = {'username':'gh_willbullen', 'password':'B@ff1ed!2020'}

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
        # SET PAGE DATA
        query = Nodes.objects.filter(Type = Node_Type.objects.only('id').get(Type_Name=self.db_name).id)
        for node in query.iterator():
            self.get_HistoryData(node.id)
            self.get_CurrentData(node.id)
            self.get_StatusData(node.id)
            self.get_SetupData(node.id)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        jsonData = json.loads(text_data)
        if jsonData['Node'] == 'Picarro':
            if jsonData['Module'] == 'Heartbeat':
                if jsonData['Action'] == 'Update':
                    # GET NODE ID
                    Node_ID = Nodes.objects.only('id').get(Node_ID = jsonData['Node_ID']).id
                    # STATUS
                    Status = 0
                    AssetStatus = 0
                    NodeStatus = 0
                    AssetStatusDescription = ''
                    NodeStatusDescription = ''
                    # NODE STATUS
                    balena = Balena()                    
                    try:
                        balena.auth.login(**self.balenaCredentials)
                        nodeData = balena.models.device.get(Nodes.objects.only('Node_Device_ID').get(id = Node_ID).Node_Device_ID)
                        if nodeData['api_heartbeat_state'] == 'Offline':
                            NodeStatus = 1
                            NodeStatusDescription = 'Node currently offline.'
                        else:
                            NodeStatus = 0
                            NodeStatusDescription = 'Node online.'
                    except Exception as e:
                        print('{!r}; Get node status failed - '.format(e))
                    # ASSET STATUS
                    AssetStatusDescription = ''
                    if (jsonData['Data_SerialStatus'] > 0 or jsonData['Data_MetStatus'] > 0):
                        AssetStatus = 1
                    else:
                        AssetStatus = 0
                    if (jsonData['Data_SerialStatus'] == 0 and jsonData['Data_MetStatus'] == 0): # PICARRO
                        AssetStatusDescription += 'Asset OK. '
                    elif (jsonData['Data_SerialStatus'] == 1):
                        AssetStatusDescription += 'No serial connection with Picarro. '
                    elif (jsonData['Data_SerialStatus'] == 2):
                        AssetStatusDescription += 'Serial data array error. '
                    elif (jsonData['Data_SerialStatus'] == 3):
                        AssetStatusDescription += 'Serial data length > 250. '
                    elif (jsonData['Data_SerialStatus'] == 4):
                        AssetStatusDescription += 'Serial connection established but no data. '
                    if (jsonData['Data_SerialStatus'] == 0 and jsonData['Data_MetStatus'] == 0): # MET
                        AssetStatusDescription += 'Asset OK. '
                    elif (jsonData['Data_MetStatus'] == 1):
                        AssetStatusDescription += 'No connection with Met data logger. '
                    elif (jsonData['Data_MetStatus'] == 2):
                        AssetStatusDescription += 'Connected but no new data from instuments. '
                    # OVERALL STATUS
                    if (AssetStatus > 0 or NodeStatus > 0):
                        Status = 1
                    else:
                        Status = 0
                    # SAVE STATUS DATA
                    try:
                        Nodes.objects.filter(id=Node_ID).update(Status = Status, Asset_Status = AssetStatus, Asset_Status_Description = AssetStatusDescription, Node_Status = NodeStatus, Node_Status_Description = NodeStatusDescription)
                        print('Node ID: {!r} - Node Status Updated.'.format(Node_ID))
                        print("Status: " + str(Status) + "\n Asset Status: " + str(AssetStatus) + "\n Node Status:" + str(NodeStatus) + "\n AssetStatus Description:" + AssetStatusDescription + "\n NodeStatus Description:" + NodeStatusDescription)
                    except Exception as e:
                        print('{!r}; Save status failed - '.format(e))
                    # SAVE NODE DATA
                    try:
                        if (jsonData['Data_DateTime'] != self.datetime_check_picarro and jsonData['Data_CO2'] != ''):
                            Picarro_Data.objects.create(
                                # NODE ID
                                Node_ID=Nodes.objects.get(Node_ID=jsonData['Node_ID']),
                                # DATETIME STAMP
                                Data_DateTime=jsonData['Data_DateTime'],
                                # SERIAL DATA VARIABLES
                                Data_CO2=jsonData['Data_CO2'],
                                Data_CO2_Dry=jsonData['Data_CO2_Dry'],
                                Data_CO=jsonData['Data_CO'],
                                Data_CH4=jsonData['Data_CH4'],
                                Data_CH4_Dry=jsonData['Data_CH4_Dry'],
                                Data_H2O=jsonData['Data_H2O'],
                                Data_Amb_P=jsonData['Data_Amb_P'],
                                Data_CavityPressure=jsonData['Data_CavityPressure'],
                                Data_Cavity_Temp=jsonData['Data_Cavity_Temp'],
                                Data_DasTemp=jsonData['Data_DasTemp'],
                                Data_EtalonTemp=jsonData['Data_EtalonTemp'],
                                Data_WarmBoxTemp=jsonData['Data_WarmBoxTemp'],
                                Data_Species=jsonData['Data_Species'],
                                Data_MPVPosition=jsonData['Data_MPVPosition'],
                                Data_OutletValve=jsonData['Data_OutletValve'],
                                Data_Solenoid_Valves=jsonData['Data_Solenoid_Valves'],
                                Data_h2o_reported=jsonData['Data_h2o_reported'],
                                Data_b_h2o_pct=jsonData['Data_b_h2o_pct'],
                                Data_peak_14=jsonData['Data_peak_14'],
                                Data_peak84_raw=jsonData['Data_peak84_raw'],
                                # METEORLOGICAL DATA VARIABLES
                                Data_MaxGust=jsonData['Data_MaxGust'],
                                Data_MaxGustDir=jsonData['Data_MaxGustDir'],
                                Data_WindDir=jsonData['Data_WindDir'],
                                Data_WindSpeed=jsonData['Data_WindSpeed'],
                                Data_Pressure=jsonData['Data_Pressure'],
                                Data_DryA=jsonData['Data_DryA'],
                                Data_GrassA=jsonData['Data_GrassA'],
                                Data_HumA=jsonData['Data_HumA'],
                                # INSTRUMENT DATA VARIABLES
                                Instrument_Supply_Voltage=jsonData['Instrument_Supply_Voltage'],
                                Instrument_Supply_Current=jsonData['Instrument_Supply_Current'],
                                Instrument_Temp=jsonData['Instrument_Temp'],
                                Instrument_Pressure=jsonData['Instrument_Pressure'],
                                Instrument_Humidity=jsonData['Instrument_Humidity'],
                                Instrument_Status=jsonData['Instrument_Status']
                            )
                        self.datetime_check_picarro = jsonData['Data_DateTime']
                    except Exception as e:
                        print('{!r}; Save node data failed - '.format(e))
                    
                    self.get_HistoryData(Node_ID)
                    self.get_CurrentData(Node_ID)
                    self.get_StatusData(Node_ID)

    def stream_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))

    def get_HistoryData(self, node_id):
        History = {}
        try:            
            History['Data'] = json.loads(Picarro_Data.objects.filter(Node_ID=node_id).order_by('-id')[:1440].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('10Min').mean().fillna(method='backfill').tail(140).to_json(orient="table"))
            History['Data_Type'] = "HistoryData"
            History['Node_ID'] = node_id            
        except Exception as e:
            print('{!r}; Get history data failed - '.format(e))
        else:
            self.async_send(self.group_name, History)

    def get_CurrentData(self, node_id):
        Current = {}
        try:            
            Current['Data'] = {**json.loads(serializers.serialize("json", [Picarro_Data.objects.filter(Node_ID=node_id).last()]))[0]['fields']}
            Current['Data_Type'] = 'CurrentData'
            Current['Node_ID'] = node_id            
        except Exception as e:
            print('{!r}; Get current data failed - '.format(e))
        else:
            self.async_send(self.group_name, Current)

    def get_StatusData(self, node_id):
        Status = {} 
        try:
            Status['Data'] = json.loads(Nodes.objects.all().to_dataframe().to_json(orient="table"))
            Status['Data_Type'] = "StatusData"
            Status['Node_ID'] = node_id
        except Exception as e:
            print('{!r}; Get status data failed - '.format(e)) 
        else:
            self.async_send(self.group_name, Status)

    def get_SetupData(self, node_id):
        Setup = {} 
        try:
            Setup['Data'] = json.loads(Nodes.objects.filter(id=node_id).to_dataframe().to_json(orient="table"))
            Setup['Data_Type'] = "SetupData"
            Setup['Node_ID'] = node_id
        except Exception as e:
            print('{!r}; Get setup data failed - '.format(e)) 
        else:
            self.async_send(self.group_name, Setup)

class SOXConsumer(WebsocketConsumer):

    datetime_check_sox = ''

    def connect(self):
        self.room_group_name = 'sox'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print('Message Received.............')
        jsonData = json.loads(text_data)
        print(jsonData)

        if jsonData['Node'] == 'SOX':
            if jsonData['Module'] == 'Heartbeat':
                if jsonData['Action'] == 'Update':
                    # STATUS
                    if jsonData['Data_DateTime'] != self.datetime_check_sox:
                        SOX_Data.objects.create(
                            # DATETIME STAMP
                            Data_DateTime=jsonData['Data_DateTime'],
                            # SOX DATA VARIABLES
                            Data_Box_Temp=jsonData['Data_Box_Temp'],
                            Data_HVPS=jsonData['Data_HVPS'],
                            Data_Lamp_Dark=jsonData['Data_Lamp_Dark'],
                            Data_Lamp_Ratio=jsonData['Data_Lamp_Ratio'],
                            Data_Norm_PMT=jsonData['Data_Norm_PMT'],
                            Data_Photo_Absolute=jsonData['Data_Photo_Absolute'],
                            Data_PMT=jsonData['Data_PMT'],
                            Data_PMT_Dark=jsonData['Data_PMT_Dark'],
                            Data_PMT_Signal=jsonData['Data_PMT_Signal'],
                            Data_PMT_Temp=jsonData['Data_PMT_Temp'],
                            Data_Sox_Pressure=jsonData['Data_Sox_Pressure'],
                            Data_RCell_Temp=jsonData['Data_RCell_Temp'],
                            Data_Ref_4096mV=jsonData['Data_Ref_4096mV'],
                            Data_Ref_Ground=jsonData['Data_Ref_Ground'],
                            Data_REF_V_4096_Dark=jsonData['Data_REF_V_4096_Dark'],
                            Data_REF_V_4096_Light=jsonData['Data_REF_V_4096_Light'],
                            Data_Sample_Flow=jsonData['Data_Sample_Flow'],
                            Data_SO2_Concentration=jsonData['Data_SO2_Concentration'],
                            Data_Stability=jsonData['Data_Stability'],
                            Data_UV_Lamp=jsonData['Data_UV_Lamp'],
                            # METEORLOGICAL DATA VARIABLES
                            Data_MaxGust=jsonData['Data_MaxGust'],
                            Data_MaxGustDir=jsonData['Data_MaxGustDir'],
                            Data_WindDir=jsonData['Data_WindDir'],
                            Data_WindSpeed=jsonData['Data_WindSpeed'],
                            Data_Pressure=jsonData['Data_Pressure'],
                            Data_DryA=jsonData['Data_DryA'],
                            Data_GrassA=jsonData['Data_GrassA'],
                            Data_HumA=jsonData['Data_HumA'],
                            # INSTRUMENT DATA VARIABLES
                            Instrument_Supply_Voltage=jsonData['Instrument_Supply_Voltage'],
                            Instrument_Supply_Current=jsonData['Instrument_Supply_Current'],
                            Instrument_Temp=jsonData['Instrument_Temp'],
                            Instrument_Pressure=jsonData['Instrument_Pressure'],
                            Instrument_Humidity=jsonData['Instrument_Humidity'],
                            Instrument_Status=jsonData['Instrument_Status']
                        )
                    self.datetime_check_sox = jsonData['Data_DateTime']

    # Receive message from room_group
    def stream_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))


class NOXConsumer(WebsocketConsumer):

    datetime_check_nox = ''

    def connect(self):
        self.room_group_name = 'nox'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print('Message Received.............')
        jsonData = json.loads(text_data)
        print(jsonData)

        if jsonData['Node'] == 'NOX':
            if jsonData['Module'] == 'Heartbeat':
                if jsonData['Action'] == 'Update':
                    # STATUS
                    if jsonData['Data_DateTime'] != self.datetime_check_nox:
                        NOX_Data.objects.create(
                            # DATETIME STAMP
                            Data_DateTime=jsonData['Data_DateTime'],
                            # SOX DATA VARIABLES
                            Data_Box_Temp=jsonData['Data_Box_Temp'],
                            Data_HVPS=jsonData['Data_HVPS'],
                            Data_NO_Conc=jsonData['Data_NO_Conc'],
                            Data_NO_Norm_Offset=jsonData['Data_NO_Norm_Offset'],
                            Data_NO_Slope=jsonData['Data_NO_Slope'],
                            Data_NO_Stability=jsonData['Data_NO_Stability'],
                            Data_NO2_Conc=jsonData['Data_NO2_Conc'],
                            Data_NO2_Stability=jsonData['Data_NO2_Stability'],
                            Data_Norm_PMT=jsonData['Data_Norm_PMT'],
                            Data_NOX_Conc=jsonData['Data_NOX_Conc'],
                            Data_NOx_Norm_Offset=jsonData['Data_NOx_Norm_Offset'],
                            Data_NOx_Slope=jsonData['Data_NOx_Slope'],
                            Data_NOX_Stability=jsonData['Data_NOX_Stability'],
                            Data_PMT_Signal=jsonData['Data_PMT_Signal'],
                            Data_PMT_Temp=jsonData['Data_PMT_Temp'],
                            Data_Ref_4096mV=jsonData['Data_Ref_4096mV'],
                            Data_Ref_Ground=jsonData['Data_Ref_Ground'],
                            Data_Rx_Cell_Press=jsonData['Data_Rx_Cell_Press'],
                            Data_Rx_Cell_Temp=jsonData['Data_Rx_Cell_Temp'],
                            Data_Sample_Flow=jsonData['Data_Sample_Flow'],
                            Data_Sample_Press=jsonData['Data_Sample_Press'],
                            # METEORLOGICAL DATA VARIABLES
                            Data_MaxGust=jsonData['Data_MaxGust'],
                            Data_MaxGustDir=jsonData['Data_MaxGustDir'],
                            Data_WindDir=jsonData['Data_WindDir'],
                            Data_WindSpeed=jsonData['Data_WindSpeed'],
                            Data_Pressure=jsonData['Data_Pressure'],
                            Data_DryA=jsonData['Data_DryA'],
                            Data_GrassA=jsonData['Data_GrassA'],
                            Data_HumA=jsonData['Data_HumA'],
                            # INSTRUMENT DATA VARIABLES
                            Instrument_Supply_Voltage=jsonData['Instrument_Supply_Voltage'],
                            Instrument_Supply_Current=jsonData['Instrument_Supply_Current'],
                            Instrument_Temp=jsonData['Instrument_Temp'],
                            Instrument_Pressure=jsonData['Instrument_Pressure'],
                            Instrument_Humidity=jsonData['Instrument_Humidity'],
                            Instrument_Status=jsonData['Instrument_Status']
                        )
                    self.datetime_check_nox = jsonData['Data_DateTime']

    # Receive message from room_group
    def stream_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))


class BALOONConsumer(WebsocketConsumer):

    datetime_check_baloon = ''

    def connect(self):
        self.room_group_name = 'baloon'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print('Message Received.............')
        jsonData = json.loads(text_data)
        print(jsonData)

        if jsonData['Node'] == 'BALOON':
            if jsonData['Module'] == 'Heartbeat':
                if jsonData['Action'] == 'Update':
                    # STATUS
                    Data_NodeStatus = jsonData['Data_NodeStatus']
                    Data_DataStatus = jsonData['Data_DataStatus']
                    Data_InstrumentStatus = jsonData['Data_InstrumentStatus']
                    print(jsonData['Data'])
                    # if jsonData['Data_DateTime'] != self.datetime_check_baloon:
                    #    Baloon_Data.objects.create(
                    #        # DATETIME STAMP
                    #        Data_DateTime = jsonData['Data_DateTime'],
                    #        # BALOON DATA VARIABLES
                    #    )
                    #self.datetime_check_baloon = jsonData['Data_DateTime']

    # Receive message from room_group
    def stream_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))
