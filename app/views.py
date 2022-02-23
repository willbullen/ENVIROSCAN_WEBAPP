from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import json

from data.models import UPS, Generator, Autosonde_Ground_Station, Aethalometer_Data, Autosonde_Soundings, Autosonde_Sounding_Data, Autosonde_Logs, Nodes, SOX_Data, NOX_Data, Picarro_Data, Tucson_Data
from django.core import serializers

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'
    

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
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

        #Node_Type = request.GET.get('node_type')
        #Node_ID = request.GET.get('id')

        print('NODE ID: ' + Node_ID)
        print('NODE TYPE: ' + Node_Type)

        if Node_Type == 'autosonde':
            Sounding_ID = Autosonde_Soundings.objects.filter(Node_ID = Node_ID).latest('id').id                   
            context['Ground_Station_Data'] = get_groundstation_data(Node_ID, Autosonde_Ground_Station) # GROUND STATION DATA            
            context['Sounding_Data'] = get_sounding_data(Node_ID, Sounding_ID, Autosonde_Sounding_Data) # SOUNDING            
            context['Soundings_Data'] = get_soundings(Node_ID, Sounding_ID, Autosonde_Soundings) # SOUNDING DATA            
            context['Log_Data'] = get_log_data(Node_ID, Autosonde_Logs) # LOG DATA            
            context['Status_Data'] = get_status_data() # STATUS DATA            
            context['Setup_Data'] = get_setup_data(Node_ID, Nodes) # SETUP DATA
        elif Node_Type == 'sox':            
            context['History_Data'] = get_history_data(Node_ID, SOX_Data) # HISTORY            
            context['Current_Data'] = get_current_data(Node_ID, SOX_Data) # CURRENT            
            context['Status_Data'] = get_status_data() # STATUS DATA            
            context['Setup_Data'] = get_setup_data(Node_ID, Nodes) # SETUP DATA
        elif Node_Type == 'nox':            
            context['History_Data'] = get_history_data(Node_ID, NOX_Data) # HISTORY
            context['Current_Data'] = get_current_data(Node_ID, NOX_Data) # CURRENT
            context['Status_Data'] = get_status_data() # STATUS DATA
            context['Setup_Data'] = get_setup_data(Node_ID, Nodes) # SETUP DATA
        elif Node_Type == 'picarro':            
            context['History_Data'] = get_history_data(Node_ID, Picarro_Data) # HISTORY
            context['Current_Data'] = get_current_data(Node_ID, Picarro_Data) # CURRENT
            context['Status_Data'] = get_status_data() # STATUS DATA
            context['Setup_Data'] = get_setup_data(Node_ID, Nodes) # SETUP DATA
        elif Node_Type == 'tucson':            
            context['History_Data'] = get_history_data(Node_ID, Tucson_Data) # HISTORY
            context['Current_Data'] = get_current_data(Node_ID, Tucson_Data) # CURRENT
            context['Status_Data'] = get_status_data() # STATUS DATA
            context['Setup_Data'] = get_setup_data(Node_ID, Nodes) # SETUP DATA
        elif Node_Type == 'aethalometer':            
            context['History_Data'] = get_history_data(Node_ID, Aethalometer_Data) # HISTORY
            context['Current_Data'] = get_current_data(Node_ID, Aethalometer_Data) # CURRENT
            context['Status_Data'] = get_status_data() # STATUS DATA
            context['Setup_Data'] = get_setup_data(Node_ID, Nodes) # SETUP DATA
        elif Node_Type == 'ups':            
            context['History_Data'] = get_history_data(Node_ID, UPS) # HISTORY
            context['Current_Data'] = get_current_data(Node_ID, UPS) # CURRENT
            context['Status_Data'] = get_status_data() # STATUS DATA
            context['Setup_Data'] = get_setup_data(Node_ID, Nodes) # SETUP DATA
        elif Node_Type == 'generator':            
            context['History_Data'] = get_history_data(Node_ID, Generator) # HISTORY
            context['Current_Data'] = get_current_data(Node_ID, Generator) # CURRENT
            context['Status_Data'] = get_status_data() # STATUS DATA
            context['Setup_Data'] = get_setup_data(Node_ID, Nodes) # SETUP DATA
        elif Node_Type == 'daqc':            
            context['History_Data'] = get_test_data(Node_ID, SOX_Data) # HISTORY
        else:
            context['Status_Data'] = get_status_data() # STATUS DATA

        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:
        html_template = loader.get_template( 'page_404_error.html' )
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        print('{!r} - Load Template Failed!'.format(e))   
        html_template = loader.get_template( 'page_404_error.html' )
        return HttpResponse(html_template.render(context, request))

def get_test_data(node_id, object):
    test = {}
    try:
        test['Data'] = json.loads(object.objects.filter(Node_ID = node_id).order_by('-id')[:5000].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('10Min').mean().fillna(method='backfill').to_json(orient="table"))
        test['Data_Type'] = "HistoryData"
        test['Node_ID'] = node_id
    except Exception as e:
        print('{!r}; Get History data failed - '.format(e))
    return json.dumps(test)

def get_setup_data(node_id, object):
    Setup = {}
    try:
        Setup['Data'] = json.loads(object.objects.filter(id = node_id).to_dataframe().to_json(orient="table"))
        Setup['Data_Type'] = "SetupData"
        Setup['Node_ID'] = node_id
    except Exception as e:
        print('{!r}; Get Setup data failed - '.format(e))
    return json.dumps(Setup)

def get_status_data():
    Status = {}
    try:
        Status['Data'] = json.loads(Nodes.objects.all().to_dataframe().to_json(orient="table"))
        Status['Data_Type'] = "StatusData"
        Status['Node_ID'] = 0
    except Exception as e:
        print('{!r}; Get Status data failed - '.format(e))
    return json.dumps(Status)

def get_current_data(node_id, object):
    Current = {}
    try:
        Current['Data'] = {**json.loads(serializers.serialize("json", [object.objects.filter(Node_ID = node_id).last()]))[0]['fields']}
        Current['Data_Type'] = 'CurrentData'
        Current['Node_ID'] = node_id
    except Exception as e:
        print('{!r}; Get Current data failed - '.format(e))
    return json.dumps(Current)

def get_history_data(node_id, object):
    History = {}
    try:
        History['Data'] = json.loads(object.objects.filter(Node_ID = node_id).order_by('-id')[:1440].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('10Min').mean().fillna(method='backfill').tail(140).to_json(orient="table"))
        History['Data_Type'] = "HistoryData"
        History['Node_ID'] = node_id
    except Exception as e:
        print('{!r}; Get History data failed - '.format(e))
    return json.dumps(History)

def get_groundstation_data(node_id, object):
    Ground_Station = {}
    try:
        Ground_Station['Data'] = json.loads(object.objects.filter(Node_ID = node_id).order_by('-id')[:1440].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('10Min').mean().fillna(method='backfill').tail(140).to_json(orient="table"))
        Ground_Station['Data_Type'] = "GroundstationData"
        Ground_Station['Node_ID'] = node_id
    except Exception as e:
        print('{!r}; Get Groundstation data failed - '.format(e))
    return json.dumps(Ground_Station)

def get_sounding_data(node_id, sounding_id, object):
    Sounding = {}
    try:
        Sounding['Data'] = json.loads(object.objects.filter(Sounding_ID = sounding_id).to_dataframe().to_json(orient="table"))
        Sounding['Data_Type'] = 'SoundingData'
        Sounding['Node_ID'] = node_id    
        Sounding['Sounding_ID'] = sounding_id
    except Exception as e:
        print('{!r}; Get Sounding data failed - '.format(e))
    return json.dumps(Sounding)

def get_soundings(node_id, sounding_id, object):
    Soundings = {}
    try:
        Soundings['Data'] = {**json.loads(serializers.serialize("json", [object.objects.filter(Node_ID = node_id).latest('id')]))[0]['fields']}
        Soundings['Data_Type'] = 'SoundingsData'
        Soundings['Node_ID'] = node_id  
        Soundings['Sounding_ID'] = sounding_id
    except Exception as e:
        print('{!r}; Get Soundings data failed - '.format(e))
    return json.dumps(Soundings)

def get_log_data(node_id, object):
    Logs = {}
    try:
        Logs['Data'] = json.loads(object.objects.filter(Node_ID = node_id).to_dataframe().to_json(orient="table"))
        Logs['Data_Type'] = 'LogData'
        Logs['Node_ID'] = node_id
    except Exception as e:
        print('{!r}; Get Log data failed - '.format(e))
    return json.dumps(Logs)