from django.urls import include, path, re_path
from rest_framework import routers
from . import views

routerNodePower = routers.DefaultRouter()
routerNodePower.register(r'data', views.Node_Power_ViewSet)
routerNodePower.register(r'get_by_id_and_dates', views.GetPowerDataByIdAndDates_ViewSet, basename="get_by_id_and_dates")
routerNodePower.register(r'insert', views.Insert_ViewSet, basename="insert")

routerNodeTemperature = routers.DefaultRouter()
routerNodeTemperature.register(r'data', views.Node_Temperature_ViewSet)
routerNodeTemperature.register(r'get_by_id_and_dates', views.GetTemperatureDataByIdAndDates_ViewSet, basename="get_by_id_and_dates")
routerNodeTemperature.register(r'insert', views.Insert_Temperature_ViewSet, basename="insert")

routerNodes = routers.DefaultRouter()
routerNodes.register(r'list', views.Node_List_ViewSet)

urlpatterns = [

    path('node_power/', include(routerNodePower.urls)),
    path('node_temperature/', include(routerNodeTemperature.urls)),
    path('node/', include(routerNodes.urls)),

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]