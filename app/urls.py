# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [

    # cmms
    path('cmms/', views.cmms, name='cmms'),

    # daqc
    path('daqc/', views.daqc, name='daqc'),

    # picarro
    path('picarro_dash/', views.picarro, name='picarro'),

    # aethalometer
    path('aethalometer_dash/', views.aethalometer, name='aethalometer'),

    # sox
    path('sox_dash/', views.sox, name='sox'),

    # nox
    path('nox_dash/', views.nox, name='nox'),

    # autosonde
    path('autosonde_dash/', views.autosonde, name='autosonde'),

    # tucson
    path('tucson_dash/', views.tucson, name='tucson'),

    # generator
    path('generator_dash/', views.generator, name='generator'),

    # ups
    path('ups_dash/', views.ups, name='ups'),

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]