from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import json

from rest_framework import pagination

from rest_framework import viewsets
from rest_framework.response import Response

from .models import (
    Node_Power,
    Node_List,
    Node_Temperature
)

from .serializers import (
    Power_Serializer,
    Temperature_Serializer,
    Node_List_Serializer,
)

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Node_Power_ViewSet(viewsets.ModelViewSet):
    queryset = Node_Power.objects.all().order_by('Data_DateTime')
    serializer_class = Power_Serializer

class Node_Temperature_ViewSet(viewsets.ModelViewSet):
    queryset = Node_Temperature.objects.all().order_by('Data_DateTime')
    serializer_class = Temperature_Serializer

class Node_List_ViewSet(viewsets.ModelViewSet):
    queryset = Node_List.objects.all()
    serializer_class = Node_List_Serializer
    def list(self, request):
        data = json.loads(get_power_nodes())
        return Response(data)
    
######### TEMPERATURE
# url = 'dalys/node_temperature/get_by_id_and_dates/?node_id=' + str(self.ID) + '&start_datetime=' + start_datetime + '&end_datetime=' + end_datetime + ''
class GetTemperatureDataByIdAndDates_ViewSet(viewsets.ModelViewSet):
    serializer_class = Temperature_Serializer
    pagination.PageNumberPagination.page_size = 100000
    def get_queryset(self):
        node_id = self.request.query_params.get('node_id')
        start_datetime = self.request.query_params.get('start_datetime')
        end_datetime = self.request.query_params.get('end_datetime')

        return Node_Temperature.objects.filter(Node = node_id, Data_DateTime__gte = start_datetime, Data_DateTime__lte = end_datetime).order_by('-id')

class Insert_Temperature_ViewSet(viewsets.ModelViewSet):
    queryset = Node_Temperature.objects.all().order_by('Data_DateTime')
    serializer_class = Temperature_Serializer

    def create(self, request):
        # Data Format: {'uplink_message': {'decoded_payload': {'Data_DateTime': '2022-09-13T13:18:25.903Z', 'Meter_Id': 1, 'Battery_MV': 4007, 'Battery_Percent': 88, 'Temperature': -14.98}}}  
        data = request.data['uplink_message']['decoded_payload']

        print(self.request.data)        

        channel_name = 'temperature'
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': data})
        
        msg_temperature_readings = Node_Temperature.objects.create(
            Node = Node_List.objects.get(id = data['Meter_Id']),
            Data_DateTime = data['Data_DateTime'],
            Battery_MV = data['Battery_MV'],
            Battery_Percent = data['Battery_Percent'],
            Temperature = data['Temperature']
        )
        
        return Response(data = "done")

######### POWER
# url = 'dalys/node_power/get_by_id_and_dates/?node_id=' + str(self.ID) + '&start_datetime=' + start_datetime + '&end_datetime=' + end_datetime + ''
class GetPowerDataByIdAndDates_ViewSet(viewsets.ModelViewSet):
    serializer_class = Power_Serializer
    pagination.PageNumberPagination.page_size = 100000
    def get_queryset(self):
        node_id = self.request.query_params.get('node_id')
        start_datetime = self.request.query_params.get('start_datetime')
        end_datetime = self.request.query_params.get('end_datetime')

        return Node_Power.objects.filter(Node = node_id, Data_DateTime__gte = start_datetime, Data_DateTime__lte = end_datetime).order_by('-id')

class Insert_ViewSet(viewsets.ModelViewSet):
    queryset = Node_Power.objects.all().order_by('Data_DateTime')
    serializer_class = Power_Serializer

    def create(self, request):
        # Data Format: {'uplink_message': {'decoded_payload': {'Data_DateTime': '2022-09-13T13:18:25.903Z', 'Meter_Id': 1, 'Pulse_Count': 407, 'Pulses': 0}}}  
        data = request.data['uplink_message']['decoded_payload']

        print(self.request.data)   

        channel_name = 'power'
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(channel_name, {"type": "stream.message", 'message': data})    
        
        msg_meter_readings = Node_Power.objects.create(
            Node = Node_List.objects.get(id = data['Meter_Id']),
            Data_DateTime = data['Data_DateTime'],
            RealPower_L1 = data['Realpower1'],
            RealPower_L2 = data['Realpower2'],
            RealPower_L3 = data['Realpower3'],
            AppaPower_L1 = data['ApparentPower1'],
            AppaPower_L2 = data['ApparentPower2'],
            AppaPower_L3 = data['ApparentPower3'],
            Irms_L1 = data['Irms1'],
            Irms_L2 = data['Irms2'],
            Irms_L3 = data['Irms3'],
            Vrms_L1 = data['Vrms1'],
            Vrms_L2 = data['Vrms2'],
            Vrms_L3 = data['Vrms3'],
            PowerFact_L1 = data['PowerFactor1'],
            PowerFact_L2 = data['PowerFactor2'],
            PowerFact_L3 = data['PowerFactor3']
        )
        
        return Response(data = "done")

@login_required(login_url="/login/")
def index(request):
    context = {}

    print('trest')

    context['node_list_data'] = get_power_nodes()
    context['node_list_supply'] = Node_List.objects.filter(Category = 3)
    context['node_list_consumer'] = Node_List.objects.filter(Category = 1)
    context['node_list_distribution'] = Node_List.objects.filter(Category = 2)
    #context['node_list'] = json.loads(get_power_nodes())
    
    context['segment'] = 'index'
    html_template = loader.get_template('app_dalys/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def mobile(request):
    context = {}

    print('mobile')

    context['node_data'] = get_nodes()
    context['node_list'] = Node_List.objects.all().order_by('-Type')
    #context['node_list'] = json.loads(get_power_nodes())
    
    context['segment'] = 'mobile'
    html_template = loader.get_template('app_dalys/mobile.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template
        context['test'] = 'this is a testicle...'

        if request.method == 'GET' and 'node_type' in request.GET:
            Node_Type = request.GET['node_type']
        else:
            Node_Type = 'none'

        if request.method == 'GET' and 'id' in request.GET:
            Node_ID = request.GET['id']
        else:
            Node_ID = '0'

        print('NODE ID: ' + Node_ID)
        print('NODE TYPE: ' + Node_Type)

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('page_404_error.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        print('{!r} - Load Template Failed!'.format(e))
        html_template = loader.get_template('page_404_error.html')
        return HttpResponse(html_template.render(context, request))

def get_power_nodes():
    nodes = {}
    try:
        nodes['Data'] = json.loads(Node_List.objects.filter(Type = 1).order_by('Category').to_dataframe().to_json(orient="table"))['data']
        for node in nodes['Data']:
            node.update(get_power_history(node['id']))
            #node.update(get_report(node['id']))            
            node.update(get_power_latest(node['id']))
            #node.update(get_baseline(node['id']))
    except Exception as e:
        print('{!r}; Get Nodes failed - '.format(e))
    return json.dumps(nodes)

def get_nodes():
    nodes = {}
    try:
        nodes['Data'] = json.loads(Node_List.objects.all().order_by('Category').to_dataframe().to_json(orient="table"))['data']
        for node in nodes['Data']:
            print(node['Type'])
            if node['Type'] == 'Temperature':
                #node.update(get_temperature_history(node['id']))
                node.update(get_temperature_latest(node['id']))
            elif node['Type'] == 'Power':
                #node.update(get_power_history(node['id']))    
                node.update(get_power_latest(node['id']))
    except Exception as e:
        print('{!r}; Get Nodes failed - '.format(e))
    return json.dumps(nodes)

def get_report(node_id):
    try:  
        report = {'report': json.loads(Node_Power.objects.filter(Node = node_id).order_by('-id').to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('1D').mean().fillna(method='backfill').to_json(orient="table"))['data']}
    except Exception as e:
        print('{!r}; Get Report failed - '.format(e))
        return {'report': []}
    return report

def get_temperature_history(node_id):
    try:
        history = {'history': json.loads(Node_Temperature.objects.filter(Node = node_id).order_by('-id')[:12000].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('10Min').mean().fillna(method='backfill').to_json(orient="table"))['data']}
    except Exception as e:
        print('{!r}; Get temperature history failed - '.format(e))
        return {'history': []}
    return history

def get_power_history(node_id):
    try:
        history = {'history': json.loads(Node_Power.objects.filter(Node = node_id).order_by('-id')[:12000].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('10Min').mean().fillna(method='backfill').to_json(orient="table"))['data']}
    except Exception as e:
        print('{!r}; Get power history failed - '.format(e))
        return {'history': []}
    return history

def get_temperature_latest(node_id):
    try:
        latest = json.loads(Node_Temperature.objects.filter(Node = node_id).values('Data_DateTime', 'Battery_MV', 'Battery_Percent', 'Temperature').order_by('-id')[:1].to_dataframe(index='Data_DateTime').sort_index(ascending=True).to_json(orient="table"))['data'][0]
    except Exception as e:
        print('{!r}; Get latest Readings failed - '.format(e))
        return {'latest': []}
    return latest

def get_power_latest(node_id):
    try:
        latest = json.loads(Node_Power.objects.filter(Node = node_id).values('Data_DateTime', 'AppaPower_L1', 'AppaPower_L2', 'AppaPower_L3', 'Irms_L1', 'Irms_L2', 'Irms_L3', 'Vrms_L1', 'Vrms_L2', 'Vrms_L3', 'PowerFact_L1', 'PowerFact_L2', 'PowerFact_L3', 'RealPower_L1', 'RealPower_L2', 'RealPower_L3').order_by('-id')[:1].to_dataframe(index='Data_DateTime').sort_index(ascending=True).to_json(orient="table"))['data'][0]
    except Exception as e:
        print('{!r}; Get latest Readings failed - '.format(e))
        return {'latest': []}
    return latest

def get_baseline(node_id):    
    try:
        df = Node_Power.objects.filter(Node = node_id).order_by('-id').to_dataframe(index='Data_DateTime').rename_axis('Hour')        
        baseline = {'baseline': json.loads(df.groupby(df.index.hour).mean().to_json(orient="table"))['data']}
    except Exception as e:
        print('{!r}; Get baseline failed - '.format(e))
        return {'baseline': []}
    return baseline