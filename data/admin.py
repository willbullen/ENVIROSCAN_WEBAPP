from django.contrib import admin
from .models import UPS, Generator, Autosonde_Ground_Station, Autosonde_Logs, Autosonde_Sounding_Data, Autosonde_Soundings, Clients, Node_Category, Nodes, Node_Location, Node_Type, SOX_Data, NOX_Data, Defib_Data, Picarro_Data, Picarro_Logs, Aethalometer_Data, Aethalometer_Logs, Weather_Data, Weather_Logs, Tucson_Data, Tucson_Logs, Baloon_Data, Baloon_Logs, Picarro_PM, Picarro_Jobs, Picarro_Properties, Picarro_Alarms, Picarro_Property_Types
from .models import CMMS_Job_Priority, CMMS_Job_Schedule_Period, CMMS_Job_Schedule_Type, CMMS_Job_Status, CMMS_Job_Types, CMMS_Jobs, CMMS_Job_Tasks, CMMS_Job_Attachments
from .models import DAQC_Fields, DAQC_Change_Log

admin.site.register(Aethalometer_Data)
admin.site.register(Aethalometer_Logs)
admin.site.register(Picarro_Data)
admin.site.register(Picarro_Logs)
admin.site.register(Picarro_Alarms)
admin.site.register(Picarro_PM)
admin.site.register(Picarro_Jobs)
admin.site.register(Picarro_Properties)
admin.site.register(Picarro_Property_Types)
admin.site.register(Weather_Data)
admin.site.register(Weather_Logs)
admin.site.register(Tucson_Data)
admin.site.register(Tucson_Logs)
admin.site.register(Baloon_Data)
admin.site.register(Baloon_Logs)
#admin.site.register(Kraken_Data)
admin.site.register(Defib_Data)
admin.site.register(SOX_Data)
admin.site.register(NOX_Data)
admin.site.register(Nodes)
admin.site.register(Node_Type)
admin.site.register(Node_Location)
admin.site.register(Node_Category)
admin.site.register(Clients)
admin.site.register(Autosonde_Logs)
admin.site.register(Autosonde_Sounding_Data)
admin.site.register(Autosonde_Soundings)
admin.site.register(Autosonde_Ground_Station)
admin.site.register(UPS)
admin.site.register(Generator)

########### CMMS ##############
admin.site.register(CMMS_Job_Priority)
admin.site.register(CMMS_Job_Schedule_Period)
admin.site.register(CMMS_Job_Schedule_Type)
admin.site.register(CMMS_Job_Status)
admin.site.register(CMMS_Job_Types)
admin.site.register(CMMS_Jobs)
admin.site.register(CMMS_Job_Tasks)
admin.site.register(CMMS_Job_Attachments)

########### DAQC ##############
admin.site.register(DAQC_Fields)
admin.site.register(DAQC_Change_Log)