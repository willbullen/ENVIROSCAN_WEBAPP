from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import json
import pandas as pd

from rest_framework import viewsets
from rest_framework.response import Response

from .models import (
    Meter_List,
    Water_Meter,
)

from .serializers import (
    Meter_List_Serializer,
    Readings_Serializer,
)

from data.models import (
    SOX_Data,
)

class Readings_ViewSet(viewsets.ModelViewSet):
    queryset = Water_Meter.objects.all().order_by('Data_DateTime')
    serializer_class = Readings_Serializer

class Meter_List_ViewSet(viewsets.ModelViewSet):
    queryset = Meter_List.objects.all()
    serializer_class = Meter_List_Serializer

    def list(self, request):
        data = json.loads(get_meters())
        return Response(data)

    def create(self, request):
        print(request.data)

@login_required(login_url="/login/")
def index(request):

    context = {}

    context['meter_list_data'] = get_meters()
    context['meter_list_supply'] = Meter_List.objects.filter(Category = 1)
    context['meter_list_consumer'] = Meter_List.objects.filter(Category = 2)
    context['meter_list_waste'] = Meter_List.objects.filter(Category = 3)
    #context['meter_list'] = json.loads(get_meters())

    html_template = loader.get_template( 'app_water/index.html' )
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

        html_template = loader.get_template('app_water/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('page_404_error.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        print('{!r} - Load Template Failed!'.format(e))
        html_template = loader.get_template('page_404_error.html')
        return HttpResponse(html_template.render(context, request))

def get_meters():
    meters = {}
    try:
        meters['Data'] = json.loads(Meter_List.objects.all().order_by('Category').to_dataframe().to_json(orient="table"))['data']
        for meter in meters['Data']:
            meter.update(get_readings(meter['id']))
            meter.update(get_report(meter['id']))
            meter.update(get_baseline(meter['id']))
    except Exception as e:
        print('{!r}; Get Meters failed - '.format(e))
    return json.dumps(meters)

def get_report(meter_id):
    try:
        report = {'report': json.loads(Water_Meter.objects.filter(Meter = meter_id).order_by('-id').to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('1D').sum().fillna(method='backfill').to_json(orient="table"))['data']}
    except Exception as e:
        print('{!r}; Get Report failed - '.format(e))
        return {'report': []}
    return report

def get_readings(meter_id):    
    try:
        readings = {'readings': json.loads(Water_Meter.objects.filter(Meter = meter_id).order_by('-id')[:5000].to_dataframe(index='Data_DateTime').sort_index(ascending=True).resample('60Min').sum().fillna(method='backfill').to_json(orient="table"))['data']}
    except Exception as e:
        print('{!r}; Get Readings failed - '.format(e))
        return {'readings': []}
    return readings

def get_baseline(meter_id):    
    try:
        df = Water_Meter.objects.filter(Meter = meter_id).order_by('-id').to_dataframe(index='Data_DateTime').rename_axis('Hour')        
        baseline = {'baseline': json.loads(df.groupby(df.index.hour).mean().to_json(orient="table"))['data']}
    except Exception as e:
        print('{!r}; Get baseline failed - '.format(e))
        return {'baseline': []}
    return baseline