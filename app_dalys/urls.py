from django.urls import include, path, re_path
from rest_framework import routers
from . import views

routerNodePower = routers.DefaultRouter()
routerNodePower.register(r'data', views.Node_Power_ViewSet)

routerNodes = routers.DefaultRouter()
routerNodes.register(r'list', views.Node_List_ViewSet)

urlpatterns = [

    path('node_power/', include(routerNodePower.urls)),
    path('node/', include(routerNodes.urls)),

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]