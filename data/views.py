from django.shortcuts import render
from rest_framework import viewsets

from .serializers import SOX_Data_Serializer, NOX_Data_Serializer, Defib_Data_Serializer, Picarro_Data_Serializer, Picarro_Logs_Serializer, Aethalometer_Data_Serializer, Aethalometer_Logs_Serializer, Weather_Data_Serializer, Weather_Logs_Serializer, Tucson_Data_Serializer, Tucson_Logs_Serializer, Baloon_Data_Serializer, Baloon_Logs_Serializer, Kraken_Data_Serializer, Picarro_PM_Serializer, Picarro_Jobs_Serializer, Picarro_Properties_Serializer, Picarro_Alarms_Serializer, Picarro_Property_Types_Serializer
from .models import SOX_Data, NOX_Data, Defib_Data, Picarro_Data, Picarro_Logs, Weather_Data, Weather_Logs, Aethalometer_Data, Aethalometer_Logs, Kraken_Data, Tucson_Data, Tucson_Logs, Baloon_Data, Baloon_Logs, Picarro_PM, Picarro_Jobs, Picarro_Properties, Picarro_Alarms, Picarro_Property_Types

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
    queryset = Picarro_Alarms.objects.all().order_by('Log_DateTime')
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