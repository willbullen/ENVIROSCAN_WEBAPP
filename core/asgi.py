import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.core.asgi import get_asgi_application
import app.routing

from django.urls import re_path

from app.consumers import StatusConsumer, HomeConsumer, PicarroConsumer, SOXConsumer, NOXConsumer, AutosondeConsumer, TucsonConsumer, AethalometerConsumer, UPSConsumer, GeneratorConsumer, DAQCConsumer

from app_dalys.consumers import DalysConsumer, TemperatureConsumer, PowerConsumer

application = ProtocolTypeRouter({    
    "http": get_asgi_application(),
    #"mqtt": consumers.MqttConsumer.as_asgi(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # app.routing.websocket_urlpatterns,
            re_path(r'^status/$', StatusConsumer.as_asgi()),
            re_path(r'^home/$',  HomeConsumer.as_asgi()),
            re_path(r'^picarro/$', PicarroConsumer.as_asgi()),
            re_path(r'^sox/$', SOXConsumer.as_asgi()),
            re_path(r'^nox/$', NOXConsumer.as_asgi()),
            re_path(r'^autosonde/$', AutosondeConsumer.as_asgi()),
            re_path(r'^tucson/$', TucsonConsumer.as_asgi()),
            re_path(r'^aethalometer/$', AethalometerConsumer.as_asgi()),
            re_path(r'^ups/$', UPSConsumer.as_asgi()),
            re_path(r'^generator/$', GeneratorConsumer.as_asgi()),
            re_path(r'^daqc/$', DAQCConsumer.as_asgi()),
            re_path(r'^dalys/$', DalysConsumer.as_asgi()),
            re_path(r'^temperature/$', TemperatureConsumer.as_asgi()),
            re_path(r'^power/$', PowerConsumer.as_asgi()),
        ])
    ),    
})