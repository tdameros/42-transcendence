from django.urls import re_path
from core import consumers

websocket_urlpatterns = [
    re_path(r'ws/notification/$', consumers.NotificationConsumer.as_asgi()),
]