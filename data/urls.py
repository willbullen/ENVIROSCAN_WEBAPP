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
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]