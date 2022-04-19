from django.urls import re_path

from . import consumers 

websocket_urlpatterns = [
    #re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'^status/$', consumers.StatusConsumer.as_asgi()),
    re_path(r'^home/$', consumers.HomeConsumer.as_asgi()),
    re_path(r'^picarro/$', consumers.PicarroConsumer.as_asgi()),
    re_path(r'^sox/$', consumers.SOXConsumer.as_asgi()),
    re_path(r'^nox/$', consumers.NOXConsumer.as_asgi()),
    re_path(r'^autosonde/$', consumers.AutosondeConsumer.as_asgi()),
    re_path(r'^tucson/$', consumers.TucsonConsumer.as_asgi()),
    re_path(r'^aethalometer/$', consumers.AethalometerConsumer.as_asgi()),
    re_path(r'^ups/$', consumers.UPSConsumer.as_asgi()),
    re_path(r'^generator/$', consumers.GeneratorConsumer.as_asgi()),
    re_path(r'^daqc/$', consumers.DAQCConsumer.as_asgi()),
]