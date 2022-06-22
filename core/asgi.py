import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.core.asgi import get_asgi_application
import app.routing

#from app.consumers import GetStatusConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            app.routing.websocket_urlpatterns
        )
    ),
    #'channel': ChannelNameRouter({
    #    "get-status": GetStatusConsumer(),
    #    #"mqtt.pub": MqttConsumer()
    #})
})