import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, SyncConsumer, WebsocketConsumer, JsonWebsocketConsumer
from data.models import Picarro_Data, Picarro_Alarms, Picarro_Logs, Picarro_Properties, Picarro_PM, Picarro_Jobs, SOX_Data, NOX_Data
import time
from time import sleep
from datetime import datetime, timezone
from django.core import serializers
from channels.layers import get_channel_layer

#from django.core.serializers.json import DjangoJSONEncoder
#from channels.db import database_sync_to_async
#from django.db.models import Count, DateTimeField
#from django.db.models.functions import Trunc
#from django_pandas.io import read_frame
#import subprocess
#import platform
#from balena import Balena
#import pandas as pd
#import app.tasks
#import threading
#from django.http import JsonResponse

class PicarroConsumer(WebsocketConsumer):

    datetime_check_picarro = ''

    def async_send(self,channel_name, jsonData):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': jsonData})

    def connect(self):
        self.room_group_name = 'valentia_picarro'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        # SEND SEED DATA SET
        self.update_Picarro()

    def disconnect(self, close_code):
        # async_to_sync(self.channel_layer.group_discard)( 
        #    self.room_group_name,
        #    self.channel_name
        # )
        #print("DISCONNECED CODE: ", close_code) 
        pass

    def receive(self, text_data):
        print('Message Received.............')
        jsonData = json.loads(text_data)
        print(jsonData)

        if jsonData['Node'] == 'Picarro':
            PicarroData = {}
            if jsonData['Module'] == 'PM':
                if jsonData['Action'] == 'Update':
                    Picarro_PM.objects.filter(id=jsonData['id']).update(
                        PM_Title=jsonData['PM_Title'], PM_Type=jsonData['PM_Type'], PM_Time_Interval=jsonData['PM_Time_Interval'], PM_Details=jsonData['PM_Details'])
                elif jsonData['Action'] == 'Add':
                    Picarro_PM.objects.create(
                        PM_DateCreated=datetime.now(), 
                        PM_Title=jsonData['PM_Title'], 
                        PM_Type=jsonData['PM_Type'], 
                        PM_Time_Interval=jsonData['PM_Time_Interval'], 
                        PM_Details=jsonData['PM_Details'],
                        PM_Task = 'app.tasks.createJob',
                        PM_Kwargs = '[]',
                        PM_Args = '[]',
                        PM_Enabled = 1,
                        PM_Last_Run_At = datetime.now(),
                        PM_Total_Run_Count = 0,
                        PM_Date_Changed = datetime.now(),
                        PM_One_Off = 0,
                    )
                    Picarro_Jobs.objects.create(
                        Jobs_DateCreated=datetime.now(),
                        Jobs_Title=jsonData['PM_Title'],
                        Jobs_Type=0,
                        Jobs_Status=1,
                        Jobs_Description=jsonData['PM_Details']
                    )

                qs_pm = Picarro_PM.objects.all().order_by('-id')
                df_pm = qs_pm.to_dataframe(index='PM_DateCreated').sort_index(ascending=True)

                qs_jobs = Picarro_Jobs.objects.all().order_by('-id')
                df_jobs = qs_jobs.to_dataframe(index='Jobs_DateCreated').sort_index(ascending=True)

                PicarroData['Data_Type'] = 'update_pm'
                PicarroData['Data_PM'] = json.loads(df_pm.to_json(orient="table"))                
                PicarroData['Data_Jobs'] = json.loads(df_jobs.to_json(orient="table"))

                async_to_sync(self.channel_layer.group_send)("valentia_picarro", {"type": "stream.message", 'message': PicarroData})

            elif jsonData['Module'] == 'Jobs':
                if jsonData['Action'] == 'Update':
                    Picarro_Jobs.objects.filter(id=jsonData['id']).update(
                        Jobs_Title=jsonData['Jobs_Title'], Jobs_Type=jsonData['Jobs_Type'], Jobs_Status=jsonData['Jobs_Status'], Jobs_Description=jsonData['Jobs_Description'])
                elif jsonData['Action'] == 'Add':
                    Picarro_Jobs.objects.create(Jobs_DateCreated=datetime.now(
                    ), Jobs_Title=jsonData['Jobs_Title'], Jobs_Type=jsonData['Jobs_Type'], Jobs_Status=jsonData['Jobs_Status'], Jobs_Description=jsonData['Jobs_Description'])

                qs_jobs = Picarro_Jobs.objects.all().order_by('-id')
                df_jobs = qs_jobs.to_dataframe(index='Jobs_DateCreated').sort_index(ascending=True)
                PicarroData['Data_Type'] = 'update_jobs'
                PicarroData['Data_Jobs'] = json.loads(df_jobs.to_json(orient="table"))

                async_to_sync(self.channel_layer.group_send)("valentia_picarro", {"type": "stream.message", 'message': PicarroData})
            
            elif jsonData['Module'] == 'Properties':                
                if jsonData['Action'] == 'Update':
                    Picarro_Properties.objects.filter(id=jsonData['id']).update(
                        Properties_Title=jsonData['Properties_Title'], Properties_Type=jsonData['Properties_Type'], Properties_Value=jsonData['Properties_Value'])
                elif jsonData['Action'] == 'Add':
                    Picarro_Properties.objects.create(Properties_DateCreated=datetime.now(
                    ), Properties_Title=jsonData['Properties_Title'], Properties_Type=jsonData['Properties_Type'], Properties_Value=jsonData['Properties_Value'])

                qs_properties = Picarro_Properties.objects.all().order_by('-id')
                df_properties = qs_properties.to_dataframe(index='Properties_DateCreated').sort_index(ascending=True)
                PicarroData['Data_Type'] = 'update_properties'
                PicarroData['Data_Properties'] = json.loads(df_properties.to_json(orient="table"))

                async_to_sync(self.channel_layer.group_send)("valentia_picarro", {"type": "stream.message", 'message': PicarroData})

            elif jsonData['Module'] == 'Heartbeat':                
                if jsonData['Action'] == 'Update':
                    print("boom bada boom.........")
                    # STATUS
                    Data_NodeStatus = jsonData['Data_NodeStatus']
                    Data_DataStatus = jsonData['Data_DataStatus']
                    Data_InstrumentStatus = jsonData['Data_InstrumentStatus']
                    if (jsonData['Data_DateTime'] != self.datetime_check_picarro and jsonData['Data_CO2'] != ''):
                        Picarro_Data.objects.create(
                            # DATETIME STAMP
                            Data_DateTime = jsonData['Data_DateTime'],
                            # SERIAL DATA VARIABLES
                            Data_CO2 = jsonData['Data_CO2'],
                            Data_CO2_Dry = jsonData['Data_CO2_Dry'],
                            Data_CO = jsonData['Data_CO'],
                            Data_CH4 = jsonData['Data_CH4'],
                            Data_CH4_Dry = jsonData['Data_CH4_Dry'],
                            Data_H2O = jsonData['Data_H2O'],
                            Data_Amb_P = jsonData['Data_Amb_P'],
                            Data_CavityPressure = jsonData['Data_CavityPressure'],
                            Data_Cavity_Temp = jsonData['Data_Cavity_Temp'],
                            Data_DasTemp = jsonData['Data_DasTemp'],
                            Data_EtalonTemp = jsonData['Data_EtalonTemp'],
                            Data_WarmBoxTemp = jsonData['Data_WarmBoxTemp'],
                            Data_Species = jsonData['Data_Species'],
                            Data_MPVPosition = jsonData['Data_MPVPosition'],
                            Data_OutletValve = jsonData['Data_OutletValve'],
                            Data_Solenoid_Valves = jsonData['Data_Solenoid_Valves'],
                            Data_h2o_reported = jsonData['Data_h2o_reported'],
                            Data_b_h2o_pct = jsonData['Data_b_h2o_pct'],
                            Data_peak_14 = jsonData['Data_peak_14'],
                            Data_peak84_raw = jsonData['Data_peak84_raw'],
                            # METEORLOGICAL DATA VARIABLES
                            Data_MaxGust = jsonData['Data_MaxGust'],
                            Data_MaxGustDir = jsonData['Data_MaxGustDir'],
                            Data_WindDir = jsonData['Data_WindDir'],
                            Data_WindSpeed = jsonData['Data_WindSpeed'],	
                            Data_Pressure = jsonData['Data_Pressure'],	
                            Data_DryA = jsonData['Data_DryA'],	
                            Data_GrassA = jsonData['Data_GrassA'],	
                            Data_HumA = jsonData['Data_HumA'],	
                            # INSTRUMENT DATA VARIABLES
                            Instrument_Supply_Voltage = jsonData['Instrument_Supply_Voltage'],
                            Instrument_Supply_Current = jsonData['Instrument_Supply_Current'],
                            Instrument_Temp = jsonData['Instrument_Temp'],
                            Instrument_Pressure = jsonData['Instrument_Pressure'],
                            Instrument_Humidity = jsonData['Instrument_Humidity'],
                            Instrument_Status = jsonData['Instrument_Status']
                        )
                    self.datetime_check_picarro = jsonData['Data_DateTime']

    # Receive message from room_group
    def stream_message(self, event):
        message = event['message']
        # print(message)
        # Send message to websocket
        self.send(text_data=json.dumps({'message': message}))

    def update_Picarro(self):

        channel_layer = get_channel_layer()

        start_timer = time.time()

        PicarroData = {}    

        ##################### TIME #######################    
        new_time = time.time()
        ##################################################

        ##################### ALARMS #####################
        PicarroAlarmData = {}
        qs_alarms = Picarro_Alarms.objects.all().order_by('-id')
        df_alarms = qs_alarms.to_dataframe(index='Alarms_DateTime').sort_index(ascending=True)
        PicarroAlarmData['Data_Alarms'] = json.loads(df_alarms.to_json(orient="table"))
        PicarroAlarmData['Data_Type'] = "update_alarms"
        self.async_send("valentia_picarro", PicarroAlarmData)

        print("--- ALARMS EXECUTION TIME: %s SECONDS ---" % (time.time() - new_time))
        new_time = time.time()
        ##################################################

        ##################### LOGS #######################
        PicarroLogData = {}
        qs_logs = Picarro_Logs.objects.all().order_by('-id')
        df_logs = qs_logs.to_dataframe(index='Log_DateTime').sort_index(ascending=True)
        PicarroLogData['Data_Logs'] = json.loads(df_logs.to_json(orient="table"))
        PicarroLogData['Data_Type'] = "update_logs"
        self.async_send("valentia_picarro", PicarroLogData)

        print("--- LOGS EXECUTION TIME: %s SECONDS ---" % (time.time() - new_time))
        new_time = time.time()
        ##################################################

        ##################### PROPERTIES #####################
        PicarroPropertyData = {}
        qs_properties = Picarro_Properties.objects.all().order_by('-id')
        df_properties = qs_properties.to_dataframe(index='Properties_DateCreated').sort_index(ascending=True)
        PicarroPropertyData['Data_Properties'] = json.loads(df_properties.to_json(orient="table"))
        PicarroPropertyData['Data_Type'] = "update_properties"
        self.async_send("valentia_picarro", PicarroPropertyData)

        print("--- PROPERTIES EXECUTION TIME: %s SECONDS ---" % (time.time() - new_time))
        new_time = time.time()
        ##################################################
        
        ##################### PM #####################
        PicarroPMData = {}
        qs_pm = Picarro_PM.objects.all().order_by('-id')
        df_pm = qs_pm.to_dataframe(index='PM_DateCreated').sort_index(ascending=True)
        PicarroPMData['Data_PM'] = json.loads(df_pm.to_json(orient="table"))
        PicarroPMData['Data_Type'] = "update_pm"
        self.async_send("valentia_picarro", PicarroPMData)

        print("--- PM EXECUTION TIME: %s SECONDS ---" % (time.time() - new_time))
        new_time = time.time()
        ##################################################

        ##################### JOBS #####################
        PicarroJobData = {}
        qs_jobs = Picarro_Jobs.objects.all().order_by('-id')
        df_jobs = qs_jobs.to_dataframe(index='Jobs_DateCreated').sort_index(ascending=True)
        PicarroJobData['Data_Jobs'] = json.loads(df_jobs.to_json(orient="table"))
        PicarroJobData['Data_Type'] = "update_jobs"
        self.async_send("valentia_picarro", PicarroJobData)

        print("--- JOBS EXECUTION TIME: %s SECONDS ---" % (time.time() - new_time))
        new_time = time.time()
        ##################################################

        ##################### CHART DATA #####################    
        qs = Picarro_Data.objects.values(
            'Data_DateTime', 
            'Data_CO2', 
            'Data_CO2_Dry', 
            'Data_CO', 
            'Data_CH4', 
            'Data_CH4_Dry', 
            'Data_H2O', 
            'Data_MPVPosition', 
            'Data_OutletValve', 
            'Data_Solenoid_Valves',

            'Data_MaxGust', 
            'Data_MaxGustDir',
            'Data_WindDir', 
            'Data_WindSpeed',
            'Data_Pressure', 
            'Data_DryA', 
            'Data_GrassA', 
            'Data_HumA',

            'Instrument_Supply_Voltage', 
            'Instrument_Supply_Current', 
            'Instrument_Temp', 
            'Instrument_Pressure', 
            'Instrument_Humidity', 
            'Instrument_Status'
            ).order_by('-id')[:1440]
            
        df = qs.to_dataframe(index='Data_DateTime').sort_index(ascending=True)
        # ------ WEEK --------
        PicarroChartData_Week = {}
        df_1w = df.resample('H').mean().fillna(method = 'backfill').tail(168)
        PicarroChartData_Week['Data_Charts_1Week'] = json.loads(df_1w.to_json(orient="table"))
        PicarroChartData_Week['Data_Type'] = "update_chart_1week"
        self.async_send("valentia_picarro", PicarroChartData_Week)

        # ------ 12 HOURS --------
        PicarroChartData_12Hours = {}
        df_12h = df.resample('10Min').mean().fillna(method = 'backfill').tail(70)
        PicarroChartData_12Hours['Data_Charts_12Hours'] = json.loads(df_12h.to_json(orient="table"))
        PicarroChartData_12Hours['Data_Type'] = "update_chart_12hour"
        self.async_send("valentia_picarro", PicarroChartData_12Hours)

        # ------ HOUR --------    
        PicarroChartData_Hour = {}
        df_1h = df.resample('Min').mean().fillna(method = 'backfill').tail(62)
        PicarroChartData_Hour['Data_Charts_1Hour'] = json.loads(df_1h.to_json(orient="table"))
        PicarroChartData_Hour['Data_Type'] = "update_chart_1hour"
        self.async_send("valentia_picarro", PicarroChartData_Hour)

        # ------ DAY --------
        PicarroChartData_Day = {}
        df_1d = df.resample('10Min').mean().fillna(method = 'backfill').tail(140)
        PicarroChartData_Day['Data_Charts_1Day'] = json.loads(df_1d.to_json(orient="table"))
        PicarroChartData_Day['Data_Type'] = "update_chart_1day"
        self.async_send("valentia_picarro", PicarroChartData_Day)

        print("--- PICARRO DATA EXECUTION TIME: %s SECONDS ---" % (time.time() - new_time))
        new_time = time.time()
        ##################################################
        
        ##################### LAST RECORD #####################

        dataPicarro_last = json.loads(serializers.serialize("json", [Picarro_Data.objects.last()]))[0]['fields']

        PicarroData['Data'] = {**dataPicarro_last}

        PicarroData['Data_Type'] = 'update'    
        
        # CHECK DATA STATUS #
        data_datetime = PicarroData['Data']['Data_DateTime']
        diff = datetime.utcnow().replace(tzinfo=timezone.utc) - datetime.strptime(data_datetime, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=timezone.utc)
        diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)
        Data_DataStatus = 0
        if diff_minutes >= 2:
            Data_DataStatus = 1

        PicarroData['Data']['Data_DataStatus'] = Data_DataStatus
        
        # CHECK STATUS #
        #balena = Balena()
        #credentials = {'username':'gh_willbullen', 'password':'B@ff1ed!2020'}
        Data_NodeStatus = 0
        #try:
        #    balena.auth.login(**credentials)
        #    nodeData = balena.models.device.get('1cbccd93410c800062b0f9e3160e33e4')
        #    if nodeData['api_heartbeat_state'] == 'Offline':
        #        Data_NodeStatus = 1
        #except Exception as e:
        #    print(e)

        PicarroData['Data']['Data_NodeStatus'] = Data_NodeStatus

        new_time = time.time()
        
        PicarroData['Data']['Data_InstrumentStatus'] = df_1h.iloc[0]['Instrument_Status']    
        
        PicarroData['HeartBeat'] = str(datetime.now())

        print("--- LAST RECORD EXECUTION TIME: %s SECONDS ---" % (time.time() - new_time))

        ##################################################
        
        print("DATA RETRIEVED AND SENT VIA WEBSOCKET ON CHANNEL STREAM.")
        print("--- TOTAL EXECUTION TIME: %s SECONDS ---" % (time.time() - start_timer))
        
        self.async_send("valentia_picarro", PicarroData)


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
                    Data_NodeStatus = jsonData['Data_NodeStatus']
                    Data_DataStatus = jsonData['Data_DataStatus']
                    Data_InstrumentStatus = jsonData['Data_InstrumentStatus']
                    if jsonData['Data_DateTime'] != self.datetime_check_sox:
                        SOX_Data.objects.create(
                            # DATETIME STAMP
                            Data_DateTime = jsonData['Data_DateTime'],
                            # SOX DATA VARIABLES
                            Data_Box_Temp  = jsonData['Data_Box_Temp'],
                            Data_HVPS  = jsonData['Data_HVPS'],
                            Data_Lamp_Dark  = jsonData['Data_Lamp_Dark'],
                            Data_Lamp_Ratio  = jsonData['Data_Lamp_Ratio'],
                            Data_Norm_PMT  = jsonData['Data_Norm_PMT'],
                            Data_Photo_Absolute  = jsonData['Data_Photo_Absolute'],
                            Data_PMT  = jsonData['Data_PMT'],
                            Data_PMT_Dark  = jsonData['Data_PMT_Dark'],
                            Data_PMT_Signal  = jsonData['Data_PMT_Signal'],
                            Data_PMT_Temp  = jsonData['Data_PMT_Temp'],
                            Data_Sox_Pressure  = jsonData['Data_Sox_Pressure'],
                            Data_RCell_Temp  = jsonData['Data_RCell_Temp'],
                            Data_Ref_4096mV  = jsonData['Data_Ref_4096mV'],
                            Data_Ref_Ground  = jsonData['Data_Ref_Ground'],
                            Data_REF_V_4096_Dark  = jsonData['Data_REF_V_4096_Dark'],
                            Data_REF_V_4096_Light  = jsonData['Data_REF_V_4096_Light'],
                            Data_Sample_Flow  = jsonData['Data_Sample_Flow'],
                            Data_SO2_Concentration  = jsonData['Data_SO2_Concentration'],
                            Data_Stability  = jsonData['Data_Stability'],
                            Data_UV_Lamp  = jsonData['Data_UV_Lamp'],       
                            # METEORLOGICAL DATA VARIABLES
                            Data_MaxGust = jsonData['Data_MaxGust'],
                            Data_MaxGustDir = jsonData['Data_MaxGustDir'],
                            Data_WindDir = jsonData['Data_WindDir'],
                            Data_WindSpeed = jsonData['Data_WindSpeed'],	
                            Data_Pressure = jsonData['Data_Pressure'],	
                            Data_DryA = jsonData['Data_DryA'],	
                            Data_GrassA = jsonData['Data_GrassA'],	
                            Data_HumA = jsonData['Data_HumA'],	
                            # INSTRUMENT DATA VARIABLES
                            Instrument_Supply_Voltage = jsonData['Instrument_Supply_Voltage'],
                            Instrument_Supply_Current = jsonData['Instrument_Supply_Current'],
                            Instrument_Temp = jsonData['Instrument_Temp'],
                            Instrument_Pressure = jsonData['Instrument_Pressure'],
                            Instrument_Humidity = jsonData['Instrument_Humidity'],
                            Instrument_Status = jsonData['Instrument_Status']
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
                    Data_NodeStatus = jsonData['Data_NodeStatus']
                    Data_DataStatus = jsonData['Data_DataStatus']
                    Data_InstrumentStatus = jsonData['Data_InstrumentStatus']
                    if jsonData['Data_DateTime'] != self.datetime_check_nox:
                        NOX_Data.objects.create(
                            # DATETIME STAMP
                            Data_DateTime = jsonData['Data_DateTime'],
                            # SOX DATA VARIABLES
                            Data_Box_Temp  = jsonData['Data_Box_Temp'],
                            Data_HVPS  = jsonData['Data_HVPS'],
                            Data_NO_Conc  = jsonData['Data_NO_Conc'],
                            Data_NO_Norm_Offset  = jsonData['Data_NO_Norm_Offset'],
                            Data_NO_Slope  = jsonData['Data_NO_Slope'],
                            Data_NO_Stability  = jsonData['Data_NO_Stability'],
                            Data_NO2_Conc  = jsonData['Data_NO2_Conc'],
                            Data_NO2_Stability  = jsonData['Data_NO2_Stability'],
                            Data_Norm_PMT  = jsonData['Data_Norm_PMT'],
                            Data_NOX_Conc  = jsonData['Data_NOX_Conc'],
                            Data_NOx_Norm_Offset  = jsonData['Data_NOx_Norm_Offset'],
                            Data_NOx_Slope  = jsonData['Data_NOx_Slope'],
                            Data_NOX_Stability  = jsonData['Data_NOX_Stability'],
                            Data_PMT_Signal  = jsonData['Data_PMT_Signal'],
                            Data_PMT_Temp  = jsonData['Data_PMT_Temp'],
                            Data_Ref_4096mV  = jsonData['Data_Ref_4096mV'],
                            Data_Ref_Ground  = jsonData['Data_Ref_Ground'],
                            Data_Rx_Cell_Press  = jsonData['Data_Rx_Cell_Press'],
                            Data_Rx_Cell_Temp  = jsonData['Data_Rx_Cell_Temp'],
                            Data_Sample_Flow  = jsonData['Data_Sample_Flow'],
                            Data_Sample_Press  = jsonData['Data_Sample_Press'],
                            # METEORLOGICAL DATA VARIABLES
                            Data_MaxGust = jsonData['Data_MaxGust'],
                            Data_MaxGustDir = jsonData['Data_MaxGustDir'],
                            Data_WindDir = jsonData['Data_WindDir'],
                            Data_WindSpeed = jsonData['Data_WindSpeed'],	
                            Data_Pressure = jsonData['Data_Pressure'],	
                            Data_DryA = jsonData['Data_DryA'],	
                            Data_GrassA = jsonData['Data_GrassA'],	
                            Data_HumA = jsonData['Data_HumA'],	
                            # INSTRUMENT DATA VARIABLES
                            Instrument_Supply_Voltage = jsonData['Instrument_Supply_Voltage'],
                            Instrument_Supply_Current = jsonData['Instrument_Supply_Current'],
                            Instrument_Temp = jsonData['Instrument_Temp'],
                            Instrument_Pressure = jsonData['Instrument_Pressure'],
                            Instrument_Humidity = jsonData['Instrument_Humidity'],
                            Instrument_Status = jsonData['Instrument_Status']
                        )
                    self.datetime_check_nox = jsonData['Data_DateTime']

    # Receive message from room_group
    def stream_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))