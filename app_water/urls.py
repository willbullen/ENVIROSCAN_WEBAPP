from django.urls import include, path, re_path
from rest_framework import routers
from . import views

routerMeters = routers.DefaultRouter()
routerMeters.register(r'list', views.Meter_List_ViewSet)

routerReadings = routers.DefaultRouter()
routerReadings.register(r'data', views.Readings_ViewSet)

urlpatterns = [

    path('meters/', include(routerMeters.urls)),

    path('readings/', include(routerReadings.urls)),

    # The home page
    path('', views.index, name='home'),

    # The home page
    path('index.html', views.index, name='home'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]