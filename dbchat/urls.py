from django.urls import path
from .views import HomeView, PrivateChatView
from django.contrib.auth.views import LoginView

app_name = 'dbchat'

urlpatterns = [
    path('', HomeView.as_view(), name = 'homepage'),
    path('login/', LoginView.as_view(template_name = 'dbchat/login.html'), name = 'login'),
    path('private_chat/<int:id>/', PrivateChatView.as_view(), name = 'private_chat'),
]

