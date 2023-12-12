from django.urls import include, path, re_path
from rest_framework import routers
from . import views

routerMeters = routers.DefaultRouter()
routerMeters.register(r'list', views.Meter_List_ViewSet)

routerReadings = routers.DefaultRouter()
routerReadings.register(r'data', views.Readings_ViewSet)
routerReadings.register(r'get_by_id_and_dates', views.GetWaterDataByIdAndDates_ViewSet, basename="get_by_id_and_dates")

routerMeterReadings = routers.DefaultRouter()
routerMeterReadings.register(r'readings', views.Meter_Readings_ViewSet)

routerPulses = routers.DefaultRouter()
routerPulses.register(r'readings', views.Pulses_ViewSet)

routerMeterReadingsAveWDH = routers.DefaultRouter()
routerMeterReadingsAveWDH.register(r'avewdh', views.Meter_Readings_Ave_WDH_ViewSet)

urlpatterns = [

    path('meters/', include(routerMeters.urls)),

    path('readings/', include(routerReadings.urls)),

    path('meter_readings/', include(routerMeterReadings.urls)),

    path('meter_readings_ave_wdh/', include(routerMeterReadingsAveWDH.urls)),

    path('pulses/', include(routerPulses.urls)),

    # The home page
    path('', views.index, name='home'),

    # The home page
    path('index.html', views.index, name='home'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]