import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courier.settings.dev')

django_asgi_app = get_asgi_application()

from apps.tracking.routing import websocket_urlpatterns as tracking_patterns
from apps.notifications.routing import websocket_urlpatterns as chat_patterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                tracking_patterns + chat_patterns
            )
        )
    ),
})