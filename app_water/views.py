from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import json
import pandas as pd

from datetime import timedelta, datetime, date

from rest_framework import viewsets
from rest_framework.response import Response

from .models import (
    Meter_List,
    Water_Meter,
    Meter_Readings,
    Meter_Readings_Ave_WDH,
)

from .serializers import (
    Meter_List_Serializer,
    Readings_Serializer,
    Meter_Readings_Serializer,
    Meter_Readings_Ave_WDH_Serializer,
)

from data.models import (
    SOX_Data,
)

class Meter_Readings_Ave_WDH_ViewSet(viewsets.ModelViewSet):
    queryset = Meter_Readings_Ave_WDH.objects.all().order_by('Last_Updated')
    serializer_class = Meter_Readings_Ave_WDH_Serializer

class Pulses_ViewSet(viewsets.ModelViewSet):
    queryset = Meter_Readings.objects.all().order_by('Data_DateTime')
    serializer_class = Meter_Readings_Serializer

    def create(self, request):
        print(self.request.data)
        
        data = request.data['data']        
        pulse_count = data['Pulse_Count'] 
        
        print(pulse_count)
        
        if (pulse_count >= 0):            
            msg_water_meter = Water_Meter.objects.create(
                Meter = Meter_List.objects.get(id = data['Meter_Id']),
                Data_DateTime = data['Data_DateTime'],
                Pulses = pulse_count, 
                Battery_Level = 100,
                Battery_Voltage = 3.3,
            )
        
        return Response(data = "done")

class Meter_Readings_ViewSet(viewsets.ModelViewSet):
    queryset = Meter_Readings.objects.all().order_by('Data_DateTime')
    serializer_class = Meter_Readings_Serializer

    def create(self, request):
        # Data Format: {'uplink_message': {'decoded_payload': {'Data_DateTime': '2022-09-13T13:18:25.903Z', 'Meter_Id': 1, 'Pulse_Count': 407, 'Pulses': 0}}}        
        data = request.data['uplink_message']['decoded_payload']
        print(self.request.data)
        pulse_count = 0
        this_pulse_count = data['Pulse_Count']

        if Meter_Readings.objects.filter(Meter_Id = data['Meter_Id']).exists():
            last_pulse_count = Meter_Readings.objects.filter(Meter_Id = data['Meter_Id']).latest('id').Pulse_Count
        else:
            last_pulse_count = 0

        if this_pulse_count < last_pulse_count:
            pulse_count = this_pulse_count
        else:
            pulse_count = this_pulse_count - last_pulse_count

        #pulse_count = this_pulse_count - last_pulse_count

        print(this_pulse_count)
        print(last_pulse_count)
        print(pulse_count)
        
        if (pulse_count >= 0):
            msg_meter_readings = Meter_Readings.objects.create(
                Meter_Id = Meter_List.objects.get(id = data['Meter_Id']),
                Data_DateTime = data['Data_DateTime'], 
                Pulse_Count = data['Pulse_Count'], 
                Pulses = pulse_count
            )
            msg_water_meter = Water_Meter.objects.create(
                Meter = Meter_List.objects.get(id = data['Meter_Id']),
                Data_DateTime = data['Data_DateTime'],
                Pulses = pulse_count, 
                Battery_Level = 100,
                Battery_Voltage = 3.3,
            )
        
        return Response(data = "done")
        
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

    context['data_analysis_data'] = get_data_analysis()

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

def get_data_analysis():
    try:
        df = pd.DataFrame(Water_Meter.objects.all().values('id', 'Data_DateTime', 'Pulses', 'Meter', 'Meter__Pulse_Unit_Value').order_by('-id')[:5000])
        df["Water"] = df["Pulses"] * df["Meter__Pulse_Unit_Value"]
        df = df.pivot_table(values='Water', index='Data_DateTime', columns='Meter', aggfunc='first').sort_index(ascending=True).resample('60Min').sum().fillna(method='backfill')
        data = json.loads(df.to_json(orient="table"))['data']
    except Exception as e:
        print('{!r}; Get data analysis data failed - '.format(e))
    return json.dumps(data)

def get_meters():
    meters = {}
    try:
        meters['Data'] = json.loads(Meter_List.objects.all().order_by('Category').to_dataframe().to_json(orient="table"))['data']
        for meter in meters['Data']:
            meter.update(get_readings(meter['id']))
            #meter.update(get_report(meter['id']))
            meter.update(get_averages(meter['id']))
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

def get_averages(meter_id):    
    try:
        result = abs(Meter_Readings_Ave_WDH.objects.only('Last_Updated').get(Meter_Id=Meter_List.objects.get(id = meter_id)).Last_Updated - datetime.now().astimezone())
        print(result.days)

        if (result.days >= 0):
            df = pd.DataFrame(Water_Meter.objects.all().values('Data_DateTime', 'Pulses', 'Meter__Pulse_Unit_Value').filter(Meter = meter_id).order_by('-id'))
            df["Water"] = df["Pulses"] * df["Meter__Pulse_Unit_Value"]
            df = df.set_index('Data_DateTime').rename_axis('DayTime')
            df = df.drop(columns=['Meter__Pulse_Unit_Value', 'Pulses'])
            #df = df.groupby([df.index.dayofweek, df.index.hour]).mean()
            df = df.groupby([df.index.dayofweek, df.index.hour]).agg({'Water': ['mean', 'min', 'max']})
            #print(df)
            #df = df.round({'Water': 3})

            print('################')
            data = []
            day = 0
            day_array = []
            for index, row in df.iterrows():
                if day == index[0]:
                    day_array.append([round(row[0], 3), round(row[1], 3), round(row[2], 3)])
                else:
                    #print(str(day) + ' - ' + str(day_array))
                    data.append(day_array)
                    day_array = []
                    day_array.append([round(row[0], 3), round(row[1], 3), round(row[2], 3)])  
                day = index[0]
            #print(str(day) + ' - ' + str(day_array))
            data.append(day_array)
            print(data[0])

            Meter_Readings_Ave_WDH.objects.update_or_create(
                Meter_Id=Meter_List.objects.get(id = meter_id), defaults={                    
                    'Last_Updated': datetime.now(), 
                    'Day_0': str(data[0]), 
                    'Day_1': str(data[1]), 
                    'Day_2': str(data[2]), 
                    'Day_3': str(data[3]), 
                    'Day_4': str(data[4]), 
                    'Day_5': str(data[5]), 
                    'Day_6': str(data[6]),                    
                }
            )
            baseline = {'baseline': json.loads(Meter_Readings_Ave_WDH.objects.filter(Meter_Id=Meter_List.objects.get(id = meter_id)).to_dataframe(index='Last_Updated').to_json(orient="table"))['data']}
        else:
            baseline = {'baseline': json.loads(Meter_Readings_Ave_WDH.objects.filter(Meter_Id=Meter_List.objects.get(id = meter_id)).to_dataframe(index='Last_Updated').to_json(orient="table"))['data']}
    except Exception as e:
        print('{!r}; Get baseline failed - '.format(e))
        return {'baseline': []}
    return baseline