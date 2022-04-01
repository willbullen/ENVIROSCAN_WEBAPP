from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import json

from rest_framework import viewsets
from .serializers import Kraken_Data_Serializer
from .models import Kraken_Data

class Kraken_Data_ViewSet(viewsets.ModelViewSet):
    queryset = Kraken_Data.objects.all().order_by('Data_DateTime')
    serializer_class = Kraken_Data_Serializer

@login_required(login_url="/login/")
def index(request):
    context = {}
    context['segment'] = 'index'
    html_template = loader.get_template('app_crypto/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        context['segment'] = load_template
        context['test'] = 'this is a testicle...'

        html_template = loader.get_template('app_crypto/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('page_404_error.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        print('{!r} - Load Template Failed!'.format(e))
        html_template = loader.get_template('page_404_error.html')
        return HttpResponse(html_template.render(context, request))
