from . import consumers
from django.urls import path

websocket_urlpatterns = [
    path('googolserver/', consumers.MyConsumer.as_asgi()),
]