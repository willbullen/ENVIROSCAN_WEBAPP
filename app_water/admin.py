from django.contrib import admin
from .models import Meter_Category, Meter_Region, Meter_Type, Meter_List, Water_Meter, Meter_Readings

admin.site.register(Meter_Category)
admin.site.register(Meter_Region)
admin.site.register(Meter_Type)
admin.site.register(Meter_List)
admin.site.register(Water_Meter)
admin.site.register(Meter_Readings)