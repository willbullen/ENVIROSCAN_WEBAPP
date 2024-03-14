from django.contrib import admin
from django.utils.html import format_html
from .models import *

class MeterListAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Organization', 'Pulse_Unit_Value', 'Pulse_Unit_Measurement', 'display_status')
    ordering = ('Organization', 'Name')

    def display_status(self, obj):
        color = 'green' if obj.Status == 0 else 'red'
        status = 'Visible' if obj.Status == 0 else 'Disabled'
        return format_html('<span style="color: {};">{}</span>', color, status)
    display_status.short_description = 'Status'  # Sets the column header

admin.site.register(Meter_Category)
admin.site.register(Meter_Region)
admin.site.register(Meter_Type)
admin.site.register(Meter_List, MeterListAdmin)
admin.site.register(Water_Meter)
admin.site.register(Meter_Readings)
admin.site.register(Meter_Readings_Ave_WDH)