from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'aethalometer_data', views.Aethalometer_Data_ViewSet)
router.register(r'aethalometer_logs', views.Aethalometer_Logs_ViewSet)
router.register(r'picarro_data', views.Picarro_Data_ViewSet)
router.register(r'picarro_logs', views.Picarro_Logs_ViewSet)
router.register(r'picarro_alarms', views.Picarro_Alarms_ViewSet)
router.register(r'picarro_pm', views.Picarro_PM_ViewSet)
router.register(r'picarro_jobs', views.Picarro_Jobs_ViewSet)
router.register(r'picarro_properties', views.Picarro_Properties_ViewSet)
router.register(r'picarro_property_types', views.Picarro_Property_Types_ViewSet)
router.register(r'weather_data', views.Weather_Data_ViewSet)
router.register(r'weather_logs', views.Weather_Logs_ViewSet)
router.register(r'tucson_data', views.Tucson_Data_ViewSet)
router.register(r'tucson_logs', views.Tucson_Logs_ViewSet)
router.register(r'baloon_data', views.Baloon_Data_ViewSet)
router.register(r'baloon_logs', views.Baloon_Logs_ViewSet)
router.register(r'kraken_data', views.Kraken_Data_ViewSet)
router.register(r'defib_data', views.Defib_Data_ViewSet)
router.register(r'sox_data', views.SOX_Data_ViewSet)
router.register(r'nox_data', views.NOX_Data_ViewSet)
router.register(r'clients', views.Clients_ViewSet)

routerUPS = routers.DefaultRouter()
routerUPS.register(r'ups_data', views.UPS_ViewSet)

routerGenerator = routers.DefaultRouter()
routerGenerator.register(r'generator_data', views.Generator_ViewSet)

routerNodes = routers.DefaultRouter()
routerNodes.register(r'node', views.Nodes_ViewSet)
routerNodes.register(r'location', views.Node_Location_ViewSet)
routerNodes.register(r'type', views.Node_Type_ViewSet)
routerNodes.register(r'category', views.Node_Category_ViewSet)

routerAutosonde = routers.DefaultRouter()
routerAutosonde.register(r'logs', views.Autosonde_Logs_ViewSet)
routerAutosonde.register(r'sounding_data', views.Autosonde_Sounding_Data_ViewSet)
routerAutosonde.register(r'soundings', views.Autosonde_Soundings_ViewSet)
routerAutosonde.register(r'ground_station_data', views.Autosonde_Ground_Station_ViewSet)
routerAutosonde.register(r'sounding', views.GetItemFromAutosondeSoundingsView, basename="autosonde_sounding")
routerAutosonde.register(r'sounding_data_bulk', views.Bulk_Create_Autosonde_Sounding_Data_ViewSet, basename="sounding_data_bulk")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('aethalometer/', include(router.urls)),
    path('picarro/', include(router.urls)),
    path('weather/', include(router.urls)),
    path('tucson/', include(router.urls)),
    path('baloon/', include(router.urls)),
    path('kraken/', include(router.urls)),
    path('defib/', include(router.urls)),
    path('nox/', include(router.urls)),
    path('sox/', include(router.urls)),
    path('nodes/', include(routerNodes.urls)),
    path('clients/', include(router.urls)),
    path('autosonde/', include(routerAutosonde.urls)),
    path('ups/', include(routerUPS.urls)),
    path('generator/', include(routerGenerator.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]