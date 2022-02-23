from django.shortcuts import render
from rest_framework import viewsets, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
import json

from .serializers import UPS_Serializer, Generator_Serializer, Autosonde_Ground_Station_Serializer, Autosonde_Logs_Serializer, Autosonde_Sounding_Data_Serializer, Autosonde_Soundings_Serializer, Node_Category_Serializer, Clients_Serializer, Nodes_Serializer, Node_Type_Serializer, Node_Location_Serializer, SOX_Data_Serializer, NOX_Data_Serializer, Defib_Data_Serializer, Picarro_Data_Serializer, Picarro_Logs_Serializer, Aethalometer_Data_Serializer, Aethalometer_Logs_Serializer, Weather_Data_Serializer, Weather_Logs_Serializer, Tucson_Data_Serializer, Tucson_Logs_Serializer, Baloon_Data_Serializer, Baloon_Logs_Serializer, Kraken_Data_Serializer, Picarro_PM_Serializer, Picarro_Jobs_Serializer, Picarro_Properties_Serializer, Picarro_Alarms_Serializer, Picarro_Property_Types_Serializer
from .models import UPS, Generator, Autosonde_Ground_Station, Autosonde_Logs, Autosonde_Sounding_Data, Autosonde_Soundings, Node_Category, Clients, Nodes, Node_Type, Node_Location, SOX_Data, NOX_Data, Defib_Data, Picarro_Data, Picarro_Logs, Weather_Data, Weather_Logs, Aethalometer_Data, Aethalometer_Logs, Kraken_Data, Tucson_Data, Tucson_Logs, Baloon_Data, Baloon_Logs, Picarro_PM, Picarro_Jobs, Picarro_Properties, Picarro_Alarms, Picarro_Property_Types

class Aethalometer_Data_ViewSet(viewsets.ModelViewSet):
    queryset = Aethalometer_Data.objects.all().order_by('Data_DateTime')
    serializer_class = Aethalometer_Data_Serializer

class Aethalometer_Logs_ViewSet(viewsets.ModelViewSet):
    queryset = Aethalometer_Logs.objects.all().order_by('Log_DateTime')
    serializer_class = Aethalometer_Logs_Serializer

class Picarro_Data_ViewSet(viewsets.ModelViewSet):
    queryset = Picarro_Data.objects.all().order_by('Data_DateTime')
    serializer_class = Picarro_Data_Serializer

class Picarro_Logs_ViewSet(viewsets.ModelViewSet):
    queryset = Picarro_Logs.objects.all().order_by('Log_DateTime')
    serializer_class = Picarro_Logs_Serializer

class Picarro_Alarms_ViewSet(viewsets.ModelViewSet):
    queryset = Picarro_Alarms.objects.all().order_by('Alarms_DateTime')
    serializer_class = Picarro_Alarms_Serializer

class Picarro_PM_ViewSet(viewsets.ModelViewSet):
    queryset = Picarro_PM.objects.all().order_by('PM_DateCreated')
    serializer_class = Picarro_PM_Serializer

class Picarro_Jobs_ViewSet(viewsets.ModelViewSet):
    queryset = Picarro_Jobs.objects.all().order_by('Jobs_DateCreated')
    serializer_class = Picarro_Jobs_Serializer

class Picarro_Properties_ViewSet(viewsets.ModelViewSet):
    queryset = Picarro_Properties.objects.all().order_by('Properties_DateCreated')
    serializer_class = Picarro_Properties_Serializer

class Picarro_Property_Types_ViewSet(viewsets.ModelViewSet):
    queryset = Picarro_Property_Types.objects.all()
    serializer_class = Picarro_Property_Types_Serializer

class Weather_Data_ViewSet(viewsets.ModelViewSet):
    queryset = Weather_Data.objects.all().order_by('Data_DateTime')
    serializer_class = Weather_Data_Serializer

class Weather_Logs_ViewSet(viewsets.ModelViewSet):
    queryset = Weather_Logs.objects.all().order_by('Log_DateTime')
    serializer_class = Weather_Logs_Serializer

class Tucson_Data_ViewSet(viewsets.ModelViewSet):
    queryset = Tucson_Data.objects.all().order_by('Data_DateTime')
    serializer_class = Tucson_Data_Serializer

class Tucson_Logs_ViewSet(viewsets.ModelViewSet):
    queryset = Tucson_Logs.objects.all().order_by('Log_DateTime')
    serializer_class = Tucson_Logs_Serializer

class Baloon_Data_ViewSet(viewsets.ModelViewSet):
    queryset = Baloon_Data.objects.all().order_by('Data_DateTime')
    serializer_class = Baloon_Data_Serializer

class Baloon_Logs_ViewSet(viewsets.ModelViewSet):
    queryset = Baloon_Logs.objects.all().order_by('Log_DateTime')
    serializer_class = Baloon_Logs_Serializer

class Kraken_Data_ViewSet(viewsets.ModelViewSet):
    queryset = Kraken_Data.objects.all().order_by('Data_DateTime')
    serializer_class = Kraken_Data_Serializer

class Defib_Data_ViewSet(viewsets.ModelViewSet):
    queryset = Defib_Data.objects.all().order_by('Data_DateTime')
    serializer_class = Defib_Data_Serializer

class NOX_Data_ViewSet(viewsets.ModelViewSet):
    queryset = NOX_Data.objects.all().order_by('Data_DateTime')
    serializer_class = NOX_Data_Serializer

class SOX_Data_ViewSet(viewsets.ModelViewSet):
    queryset = SOX_Data.objects.all().order_by('Data_DateTime')
    serializer_class = SOX_Data_Serializer

class Nodes_ViewSet(viewsets.ModelViewSet):
    queryset = Nodes.objects.all().order_by('Node_Name')
    serializer_class = Nodes_Serializer

class Node_Location_ViewSet(viewsets.ModelViewSet):
    queryset = Node_Location.objects.all().order_by('Location_Name')
    serializer_class = Node_Location_Serializer

class Node_Type_ViewSet(viewsets.ModelViewSet):
    queryset = Node_Type.objects.all().order_by('Type_Name')
    serializer_class = Node_Type_Serializer

class Node_Category_ViewSet(viewsets.ModelViewSet):
    queryset = Node_Category.objects.all().order_by('Category_Name')
    serializer_class = Node_Category_Serializer

class Clients_ViewSet(viewsets.ModelViewSet):
    queryset = Clients.objects.all().order_by('Client_Name')
    serializer_class = Clients_Serializer

class Autosonde_Logs_ViewSet(viewsets.ModelViewSet):
    queryset = Autosonde_Logs.objects.all().order_by('Log_DateTime')
    serializer_class = Autosonde_Logs_Serializer

class Autosonde_Soundings_ViewSet(viewsets.ModelViewSet):
    queryset = Autosonde_Soundings.objects.all().order_by('Data_Day')
    serializer_class = Autosonde_Soundings_Serializer

class Autosonde_Ground_Station_ViewSet(viewsets.ModelViewSet):
    queryset = Autosonde_Ground_Station.objects.all().order_by('Data_DateTime')
    serializer_class = Autosonde_Ground_Station_Serializer

class Autosonde_Sounding_Data_ViewSet(viewsets.ModelViewSet):
    queryset = Autosonde_Sounding_Data.objects.all().order_by('Data_DateTime')
    serializer_class = Autosonde_Sounding_Data_Serializer

class UPS_ViewSet(viewsets.ModelViewSet):
    queryset = UPS.objects.all().order_by('Data_DateTime')
    serializer_class = UPS_Serializer

class Generator_ViewSet(viewsets.ModelViewSet):
    queryset = Generator.objects.all().order_by('Data_DateTime')
    serializer_class = Generator_Serializer

########################################################################

class Bulk_Create_Autosonde_Sounding_Data_ViewSet(viewsets.ViewSet):
    queryset = Autosonde_Sounding_Data.objects.all()
    def create(self, request):
        print('************************************* BULK INSERT *******************************')
        post_data = request.data
        print(post_data)

        objs = [
            Autosonde_Sounding_Data(
                Sounding_ID = Autosonde_Soundings.objects.get(id = row['Sounding_ID']),
                Data_DateTime = row['Data_DateTime'],
                Data_EVSS = row['Data_EVSS'],
                Data_Pressure = row['Data_Pressure'],
                Data_Geopotential_Height = row['Data_Geopotential_Height'],
                Data_Lat = row['Data_Lat'],
                Data_Lng = row['Data_Lng'],
                Data_Air_Temperature = row['Data_Air_Temperature'],
                Data_Dewpoint_Temperature = row['Data_Dewpoint_Temperature'],
                Data_Direction = row['Data_Direction'],
                Data_Speed = row['Data_Speed']
            )
            for row in post_data
        ]
        msg = Autosonde_Sounding_Data.objects.bulk_create(objs = objs)
        #Autosonde_Sounding_Data.objects.bulk_create(post_data)
        return Response(data="return data")

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = Autosonde_Sounding_Data_Serializer(item)
        return Response(serializer.data)

    def list(self, request):
        serializer = Autosonde_Sounding_Data_Serializer(self.queryset, many=True)
        return Response(serializer.data)

class GetItemFromAutosondeSoundingsView(viewsets.ModelViewSet):
    serializer_class = Autosonde_Soundings_Serializer
    def get_queryset(self):
        node_id = self.request.query_params.get('node_id')
        sounding_day = self.request.query_params.get('sounding_day')
        sounding_type = self.request.query_params.get('sounding_type')
        sounding, created = Autosonde_Soundings.objects.get_or_create(Node_ID = Nodes.objects.get(id = node_id), Data_Day = sounding_day, Data_Type = sounding_type)
        print(created)
        return Autosonde_Soundings.objects.filter(id = sounding.id)