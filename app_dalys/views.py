from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import json

from rest_framework import viewsets
from rest_framework.response import Response

from .models import (
    Node_Power,
    Node_List,
)

from .serializers import (
    Power_Serializer,
    Node_List_Serializer,
)

class Node_Power_ViewSet(viewsets.ModelViewSet):
    queryset = Node_Power.objects.all().order_by('Data_DateTime')
    serializer_class = Power_Serializer

class Node_List_ViewSet(viewsets.ModelViewSet):
    queryset = Node_List.objects.all()
    serializer_class = Node_List_Serializer
    def list(self, request):
        data = json.loads(get_nodes())
        return Response(data)

@login_required(login_url="/login/")
def index(request):
    context = {}

    context['node_list_data'] = get_nodes()
    context['node_list_supply'] = Node_List.objects.filter(Category = 3)
    context['node_list_consumer'] = Node_List.objects.filter(Category = 1)
    context['node_list_distribution'] = Node_List.objects.filter(Category = 2)
    #context['node_list'] = json.loads(get_nodes())
    
    context['segment'] = 'index'
    html_template = loader.get_template('app_dalys/index.html')
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

def get_nodes():
    nodes = {}
    try:
        nodes['Data'] = json.loads(Node_List.objects.all().order_by('Category').to_dataframe().to_json(orient="table"))['data']
        for node in nodes['Data']:
            node.update(get_power(node['id']))
            node.update(get_report(node['id']))            
            node.update(get_latest(node['id']))
            #node.update(get_baseline(node['id']))
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

def get_power(node_id):
    try:
        history = {'history': json.loads(Node_Power.objects.filter(Node = node_id).order_by('-id')[:20000].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('10Min').mean().fillna(method='backfill').to_json(orient="table"))['data']}
    except Exception as e:
        print('{!r}; Get history failed - '.format(e))
        return {'history': []}
    return history

def get_latest(node_id):
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