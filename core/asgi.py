import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.core.asgi import get_asgi_application
import app.routing

#from app.consumers import BackgroundJobConsumer, MqttConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            app.routing.websocket_urlpatterns
        )
    ),
    'channel': ChannelNameRouter({
        #"testing-print": BackgroundJobConsumer(),
        #"mqtt.pub": MqttConsumer()
    })
})