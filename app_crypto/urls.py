from django.urls import path, re_path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'kraken_data', views.Kraken_Data_ViewSet)

urlpatterns = [

    # Data API
    path('kraken/', include(router.urls)),

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),    

]