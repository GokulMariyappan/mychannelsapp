from .views import PublicChatConsumer, PrivateChatConsumer
from django.urls import path

websocket_urlpatterns = [
    path('public_chat/', PublicChatConsumer.as_asgi()),
    path('private_chat/<int:id>/', PrivateChatConsumer.as_asgi()),
]