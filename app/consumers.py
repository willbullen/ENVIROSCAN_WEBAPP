import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, SyncConsumer, WebsocketConsumer, JsonWebsocketConsumer

from channels.db import database_sync_to_async
from data.models import Picarro_Data, Picarro_Alarms, Picarro_Logs, Picarro_Properties, Picarro_PM, Picarro_Jobs

import time
import threading
from time import sleep
from datetime import datetime, timezone

from django.core import serializers
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

from django.db.models import Count, DateTimeField
from django.db.models.functions import Trunc

from django_pandas.io import read_frame

import subprocess
import platform
from balena import Balena

import pandas as pd

import app.tasks


class PicarroConsumer(WebsocketConsumer):

    def connect(self):
        self.room_group_name = 'valentia_picarro'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        # SEND SEED DATA SET
        app.tasks.update_Picarro()

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

            async_to_sync(self.channel_layer.group_send)(
                "valentia_picarro", {"type": "stream.message", 'message': PicarroData})

    # Receive message from room_group
    def stream_message(self, event):
        message = event['message']
        # print(message)
        # Send message to websocket
        self.send(text_data=json.dumps({'message': message}))


class TucsonConsumer(WebsocketConsumer):

    def connect(self):
        self.room_group_name = 'tucson_stream'
        # Join room group
        #async_to_sync(self.channel_layer.group_add)(
        #    self.room_group_name,
        #    self.channel_name
        #)
        self.accept()
        # SEND SEED DATA SET
        #app.tasks.update_Picarro()

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

    # Receive message from room_group
    def stream_message(self, event):
        message = event['message']
        # print(message)
        # Send message to websocket
        self.send(text_data=json.dumps({'message': message}))





























































#class ChatConsumer(WebsocketConsumer):

#    def connect(self):
#        self.room_name = self.scope['url_route']['kwargs']['room_name']
#        print(self.scope['user'].username)

#        self.room_group_name = 'chat%s' % self.room_name

#        self.channel_layer.group_add(
#            self.room_group_name,
#            self.channel_name
#        )

 #       self.accept()

 #   def disconnect(self, close_code):
#        self.channel_layer.group_discard(
#            self.room_group_name,
#            self.channel_name
#        )

#    def receive(self, text_data=None, bytes_data=None):
#        text_data_json = json.loads(text_data)
#        message = text_data_json['message']
#        self.channel_layer.group_send(
#            self.room_group_name,
#            {
#                'type': 'chat_message',
#                'message': message
#            }
#        )

#    def chat_message(self, event):
#        message = event['message']
#        self.send(text_data=json.dumps({'message': message}))

#    def run_periodic_task(self):
#        while True:
#            data = Picarro_Data.objects.last().Data_CO2
#            self.send(text_data=json.dumps({'message': data}))
#            self.channel_layer.group_send(
#                self.room_group_name,
#                {
#                    'type': 'chat_message',
#                    'message': data
#                }
#            )
#            print(data)
#            time.sleep(10)

#    @database_sync_to_async
#    def get_db_data(self):
#        data = Picarro_Data.objects.last()
#        return data.Data_CO2


#class MqttConsumer(SyncConsumer):
#    def mqtt_sub(self, event):
#        topic = event['text']['topic']
#        payload = event['text']['payload']
#        # do something with topic and payload
#        print("topic: {0}, payload: {1}".format(topic, payload))

#    def mqtt_pub(self, event):
#        topic = event['text']['topic']
#        payload = event['text']['payload']
#        # do something with topic and payload
#        print("topic: {0}, payload: {1}".format(topic, payload))


#class BackgroundJobConsumer(SyncConsumer):
#    def test_print(self, message):
#        PicarroData = {}


"""
PicarroData = {}

        qs_alarms = Picarro_Alarms.objects.all().order_by('-id')
        df_alarms = qs_alarms.to_dataframe(index='Alarms_DateTime').sort_index(ascending=True)
        PicarroData['Data_Alarms'] = json.loads(df_alarms.to_json(orient="table"))

        qs_logs = Picarro_Logs.objects.all().order_by('-id')
        df_logs = qs_logs.to_dataframe(index='Log_DateTime').sort_index(ascending=True)
        PicarroData['Data_Logs'] = json.loads(df_logs.to_json(orient="table"))

        qs_properties = Picarro_Properties.objects.all().order_by('-id')
        df_properties = qs_properties.to_dataframe(index='Properties_DateCreated').sort_index(ascending=True)
        PicarroData['Data_Properties'] = json.loads(df_properties.to_json(orient="table"))
        
        qs_pm = Picarro_PM.objects.all().order_by('-id')
        df_pm = qs_pm.to_dataframe(index='PM_DateCreated').sort_index(ascending=True)
        PicarroData['Data_PM'] = json.loads(df_pm.to_json(orient="table"))

        qs_jobs = Picarro_Jobs.objects.all().order_by('-id')
        df_jobs = qs_jobs.to_dataframe(index='Jobs_DateCreated').sort_index(ascending=True)
        PicarroData['Data_Jobs'] = json.loads(df_jobs.to_json(orient="table"))

        qs = Picarro_Data.objects.all().order_by('-id')[:1440]
        df = qs.to_dataframe(index='Data_DateTime').sort_index(ascending=True) 

        # ------ 1 HOUR DATA FOR 1 WEEK --------
        df_1w = df.resample('H').mean().fillna(method = 'backfill').tail(168)
        PicarroData['Data_Charts_1Week'] = json.loads(df_1w.to_json(orient="table"))
        # ------ 10 MINUTE DATA FOR 12 HOURS --------
        df_12h = df.resample('10Min').mean().fillna(method = 'backfill').tail(72)
        PicarroData['Data_Charts_12Hours'] = json.loads(df_12h.to_json(orient="table"))
        # ------ 1 MINUTE DATA FOR 1 HOUR --------
        df_1h = df.resample('Min').mean().fillna(method = 'backfill').tail(60)
        #PicarroData['Data_Charts_1Hour'] = json.loads(df_1h[['Data_CO2', 'Data_CO', 'Data_H2O', 'Data_CH4', 'Data_CO2_Dry']].to_json(orient="table"))
        PicarroData['Data_Charts_1Hour'] = json.loads(df_1h.to_json(orient="table"))
        # ------ 20 MINUTE DATA FOR 1 DAY --------
        df_1d = df.resample('20Min').mean().fillna(method = 'backfill').tail(72)
        PicarroData['Data_Charts_1Day'] = json.loads(df_1d.to_json(orient="table"))
        # ------       LATEST RECORD      -------
        df_latest = df.tail(1)
        # CHECK DATA STATUS
        data_datetime = df_latest.index.strftime('%Y-%m-%d %H:%M').values.tolist()[0]
        diff = datetime.utcnow().replace(tzinfo=timezone.utc) - datetime.strptime(data_datetime, '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
        diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)
        Data_DataStatus = 0
        if diff_minutes >= 2:
            Data_DataStatus = 1        
        # CHECK NODE STATUS
        balena = Balena()
        credentials = {'username':'gh_willbullen', 'password':'B@ff1ed!2020'}
        Data_NodeStatus = 0
        try:
            balena.auth.login(**credentials)
            nodeData = balena.models.device.get('1cbccd93410c800062b0f9e3160e33e4')
            if nodeData['api_heartbeat_state'] == 'Offline':
                Data_NodeStatus = 1
        except Exception as e:
            print(e)
        # COMPILE AND SEND DATA ARRAY
        PicarroData['Data_Type'] = 'update'
        PicarroData['Data'] = df_latest.iloc[0].to_dict() 
        PicarroData['Data']['Data_DateTime'] = str(datetime.strptime(data_datetime, '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc))
        PicarroData['Data']['Data_NodeStatus'] = Data_NodeStatus
        PicarroData['Data']['Data_DataStatus'] = Data_DataStatus
        PicarroData['Data']['Data_InstrumentStatus'] = df_latest.iloc[0]['Instrument_Status']

        Data_Array = {}
        Data_Array['Parameter'] = list(PicarroData['Data'].keys())
        Data_Array['Value'] = list(PicarroData['Data'].values())
        picarro_df = pd.DataFrame(Data_Array)
        PicarroData['Data_Array'] = picarro_df.apply(pd.Series.explode).to_dict(orient='records')
        
        async_to_sync(self.channel_layer.group_send)(
            "stream", {"type": "stream.message", 'message': PicarroData})
"""
