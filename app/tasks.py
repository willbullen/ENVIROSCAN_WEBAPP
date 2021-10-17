from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from celery import shared_task

import json
from data.models import Picarro_Data, Picarro_Alarms, Picarro_Logs, Picarro_Properties, Picarro_PM, Picarro_Jobs, Weather_Data
import time
import threading
from time import sleep
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from django.core import serializers
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, DateTimeField
from django.db.models.functions import Trunc
from django_pandas.io import read_frame
import subprocess, platform
from balena import Balena
import pandas as pd


@shared_task
def propagate_Jobs_From_PM():
    qs_pm = Picarro_PM.objects.all().order_by('-id')

    for pm in qs_pm:
        qs_jobs = Picarro_Jobs.objects.filter(PM_id = pm.id)
        if qs_jobs:
            for job in qs_jobs:
                print(job.Jobs_Status)
                if job.Jobs_Status == 1:
                    dueDate = datetime.today()
                    if pm.PM_Type == 1:
                        dueDate = dueDate + relativedelta(hours=pm.PM_Time_Interval)
                    elif pm.PM_Type == 2:
                        dueDate = dueDate + relativedelta(days=pm.PM_Time_Interval)
                    elif pm.PM_Type == 3:
                        dueDate = dueDate + relativedelta(months=pm.PM_Time_Interval)
                    elif pm.PM_Type == 4:
                        dueDate = dueDate + relativedelta(years=pm.PM_Time_Interval)
                    print(dueDate)
                    Picarro_Jobs.objects.filter(pk=job.id).update(Jobs_Status = 2)
                    Picarro_Jobs.objects.create(
                        Jobs_DateCreated = datetime.now(),
                        Jobs_Title = pm.PM_Title,
                        Jobs_Type = 0,
                        Jobs_Status = 0,
                        Jobs_Description = pm.PM_Details,
                        PM_id = pm.id,
                        Jobs_DateToBeCompleted = dueDate,
                    )
        else:
            dueDate = datetime.today()
            if pm.PM_Type == 1:
                dueDate = dueDate + relativedelta(hours=pm.PM_Time_Interval)
            elif pm.PM_Type == 2:
                dueDate = dueDate + relativedelta(days=pm.PM_Time_Interval)
            elif pm.PM_Type == 3:
                dueDate = dueDate + relativedelta(months=pm.PM_Time_Interval)
            elif pm.PM_Type == 4:
                dueDate = dueDate + relativedelta(years=pm.PM_Time_Interval)
            print(dueDate)
            Picarro_Jobs.objects.create(
                Jobs_DateCreated = datetime.now(),
                Jobs_Title = pm.PM_Title,
                Jobs_Type = 0,
                Jobs_Status = 0,
                Jobs_Description = pm.PM_Details,
                PM_id = pm.id,
                Jobs_DateToBeCompleted = dueDate,
            )

def async_send(channel_name, jsonData):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': jsonData})

@shared_task
def update_Picarro():

    channel_layer = get_channel_layer()

    start_timer = time.time()

    PicarroData = {}    

    ##################### WEATHER #####################
    weather_qs = Weather_Data.objects.values('Data_DateTime', 'Data_MaxGust', 'Data_MaxGustDir', 'Data_MaxGustTime', 'Data_WindDir', 'Data_WindSpeed', 'Data_WindSpeed_Min', 'Data_Pressure', 'Data_DryA', 'Data_GrassA', 'Data_HumA').order_by('-id')[:10080]
    weather_df = weather_qs.to_dataframe(index='Data_DateTime').sort_index(ascending=True)
    weather_df_1w = weather_df.resample('H').mean().fillna(method = 'backfill').tail(168)
    weather_df_12h = weather_df.resample('10Min').mean().fillna(method = 'backfill').tail(70)
    weather_df_1d = weather_df.resample('20Min').mean().fillna(method = 'backfill').tail(70)
    weather_df_1h = weather_df.resample('Min').mean().fillna(method = 'backfill').tail(62)
    #PicarroData['Data_Weather_1Hour'] = json.loads(weather_df_1h.to_json(orient="table"))
    print("--- WEATHER EXECUTION TIME: %s SECONDS ---" % (time.time() - start_timer))
    new_time = time.time()
    ##################################################

    ##################### ALARMS #####################
    PicarroAlarmData = {}
    qs_alarms = Picarro_Alarms.objects.all().order_by('-id')
    df_alarms = qs_alarms.to_dataframe(index='Alarms_DateTime').sort_index(ascending=True)
    #PicarroData['Data_Alarms'] = json.loads(df_alarms.to_json(orient="table"))
    PicarroAlarmData['Data_Alarms'] = json.loads(df_alarms.to_json(orient="table"))
    PicarroAlarmData['Data_Type'] = "update_alarms"

    #async_to_sync(channel_layer.group_send)("valentia_picarro", {"type": "stream.message", 'message': PicarroAlarmData})
    async_send("valentia_picarro", PicarroAlarmData)

    print("--- ALARMS EXECUTION TIME: %s SECONDS ---" % (time.time() - new_time))
    new_time = time.time()
    ##################################################

    ##################### LOGS #####################
    PicarroLogData = {}
    qs_logs = Picarro_Logs.objects.all().order_by('-id')
    df_logs = qs_logs.to_dataframe(index='Log_DateTime').sort_index(ascending=True)
    #PicarroData['Data_Logs'] = json.loads(df_logs.to_json(orient="table"))
    PicarroLogData['Data_Logs'] = json.loads(df_logs.to_json(orient="table"))
    PicarroLogData['Data_Type'] = "update_logs"

    #async_to_sync(channel_layer.group_send)("valentia_picarro", {"type": "stream.message", 'message': PicarroLogData})
    async_send("valentia_picarro", PicarroLogData)

    print("--- LOGS EXECUTION TIME: %s SECONDS ---" % (time.time() - new_time))
    new_time = time.time()
    ##################################################

    ##################### PROPERTIES #####################
    PicarroPropertyData = {}
    qs_properties = Picarro_Properties.objects.all().order_by('-id')
    df_properties = qs_properties.to_dataframe(index='Properties_DateCreated').sort_index(ascending=True)
    #PicarroData['Data_Properties'] = json.loads(df_properties.to_json(orient="table"))
    PicarroPropertyData['Data_Properties'] = json.loads(df_properties.to_json(orient="table"))
    PicarroPropertyData['Data_Type'] = "update_properties"

    #async_to_sync(channel_layer.group_send)("valentia_picarro", {"type": "stream.message", 'message': PicarroPropertyData})
    async_send("valentia_picarro", PicarroPropertyData)

    print("--- PROPERTIES EXECUTION TIME: %s SECONDS ---" % (time.time() - new_time))
    new_time = time.time()
    ##################################################
    
    ##################### PM #####################
    PicarroPMData = {}
    qs_pm = Picarro_PM.objects.all().order_by('-id')
    df_pm = qs_pm.to_dataframe(index='PM_DateCreated').sort_index(ascending=True)
    #PicarroData['Data_PM'] = json.loads(df_pm.to_json(orient="table"))
    PicarroPMData['Data_PM'] = json.loads(df_pm.to_json(orient="table"))
    PicarroPMData['Data_Type'] = "update_pm"

    #async_to_sync(channel_layer.group_send)("valentia_picarro", {"type": "stream.message", 'message': PicarroPMData})
    async_send("valentia_picarro", PicarroPMData)

    print("--- PM EXECUTION TIME: %s SECONDS ---" % (time.time() - new_time))
    new_time = time.time()
    ##################################################

    ##################### JOBS #####################
    PicarroJobData = {}
    qs_jobs = Picarro_Jobs.objects.all().order_by('-id')
    df_jobs = qs_jobs.to_dataframe(index='Jobs_DateCreated').sort_index(ascending=True)
    #PicarroData['Data_Jobs'] = json.loads(df_jobs.to_json(orient="table"))
    PicarroJobData['Data_Jobs'] = json.loads(df_jobs.to_json(orient="table"))
    PicarroJobData['Data_Type'] = "update_jobs"

    #async_to_sync(channel_layer.group_send)("valentia_picarro", {"type": "stream.message", 'message': PicarroJobData})
    async_send("valentia_picarro", PicarroJobData)

    print("--- JOBS EXECUTION TIME: %s SECONDS ---" % (time.time() - new_time))
    new_time = time.time()
    ##################################################

    ##################### CHART DATA #####################    
    qs = Picarro_Data.objects.values('Data_DateTime', 'Data_CO2', 'Data_CO2_Dry', 'Data_CO', 'Data_CH4', 'Data_CH4_Dry', 'Data_H2O', 'Data_MPVPosition', 'Data_OutletValve', 'Data_Solenoid_Valves', 'Instrument_Supply_Voltage', 'Instrument_Supply_Current', 'Instrument_Temp', 'Instrument_Pressure', 'Instrument_Humidity', 'Instrument_Status').order_by('-id')[:10080]    
    df = qs.to_dataframe(index='Data_DateTime').sort_index(ascending=True)
    # ------ WEEK --------
    PicarroChartData_Week = {}
    df_1w = df.resample('H').mean().fillna(method = 'backfill').tail(168)
    df_1w = pd.concat([df_1w, weather_df_1w], axis=1)
    #PicarroData['Data_Charts_1Week'] = json.loads(df_1w.to_json(orient="table"))

    PicarroChartData_Week['Data_Charts_1Week'] = json.loads(df_1w.to_json(orient="table"))
    PicarroChartData_Week['Data_Type'] = "update_chart_1week"
    #async_to_sync(channel_layer.group_send)("valentia_picarro", {"type": "stream.message", 'message': PicarroChartData_Week})
    async_send("valentia_picarro", PicarroChartData_Week)

    # ------ 12 HOURS --------
    PicarroChartData_12Hours = {}
    df_12h = df.resample('10Min').mean().fillna(method = 'backfill').tail(70)
    df_12h = pd.concat([df_12h, weather_df_12h], axis=1)
    #PicarroData['Data_Charts_12Hours'] = json.loads(df_12h.to_json(orient="table"))

    PicarroChartData_12Hours['Data_Charts_12Hours'] = json.loads(df_12h.to_json(orient="table"))
    PicarroChartData_12Hours['Data_Type'] = "update_chart_12hour"
    #async_to_sync(channel_layer.group_send)("valentia_picarro", {"type": "stream.message", 'message': PicarroChartData_12Hours})
    async_send("valentia_picarro", PicarroChartData_12Hours)

    # ------ HOUR --------    
    PicarroChartData_Hour = {}
    df_1h = df.resample('Min').mean().fillna(method = 'backfill').tail(62)    
    df_1h = pd.concat([df_1h, weather_df_1h], axis=1)
    #PicarroData['Data_Charts_1Hour'] = json.loads(df_1h.to_json(orient="table"))

    PicarroChartData_Hour['Data_Charts_1Hour'] = json.loads(df_1h.to_json(orient="table"))
    PicarroChartData_Hour['Data_Type'] = "update_chart_1hour"
    #async_to_sync(channel_layer.group_send)("valentia_picarro", {"type": "stream.message", 'message': PicarroChartData_Hour})
    async_send("valentia_picarro", PicarroChartData_Hour)

    # ------ DAY --------
    PicarroChartData_Day = {}
    df_1d = df.resample('20Min').mean().fillna(method = 'backfill').tail(70)
    df_1d = pd.concat([df_1d, weather_df_1d], axis=1)
    #PicarroData['Data_Charts_1Day'] = json.loads(df_1d.to_json(orient="table"))

    PicarroChartData_Day['Data_Charts_1Day'] = json.loads(df_1d.to_json(orient="table"))
    PicarroChartData_Day['Data_Type'] = "update_chart_1day"
    #async_to_sync(channel_layer.group_send)("valentia_picarro", {"type": "stream.message", 'message': PicarroChartData_Day})    
    async_send("valentia_picarro", PicarroChartData_Day)

    print("--- PICARRO DATA EXECUTION TIME: %s SECONDS ---" % (time.time() - new_time))
    new_time = time.time()
    ##################################################
    
    ##################### LAST RECORD #####################
    PicarroLastRecordData = {}
    dataPicarro_last = json.loads(serializers.serialize("json", [Picarro_Data.objects.last()]))[0]['fields']
    dataWeather_last = json.loads(serializers.serialize("json", [Weather_Data.objects.last()]))[0]['fields']

    PicarroData['Data'] = {**dataPicarro_last, **dataWeather_last}

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

    PicarroData['Data']['Data_NodeStatus'] = Data_NodeStatus

    new_time = time.time()
    
    PicarroData['Data']['Data_InstrumentStatus'] = df_1h.iloc[0]['Instrument_Status']    
    
    PicarroData['HeartBeat'] = str(datetime.now())

    print("--- LAST RECORD EXECUTION TIME: %s SECONDS ---" % (time.time() - new_time))

    ##################################################
    
    print("DATA RETRIEVED AND SENT VIA WEBSOCKET ON CHANNEL STREAM.")
    print("--- TOTAL EXECUTION TIME: %s SECONDS ---" % (time.time() - start_timer))
    
    async_send("valentia_picarro", PicarroData)
    #async_to_sync(channel_layer.group_send)("valentia_picarro", {"type": "stream.message", 'message': PicarroData})