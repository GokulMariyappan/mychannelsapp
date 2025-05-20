from django.urls import path
from .views import HomeView, PrivateChatView,CheckUsernameView, SignUpView
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'dbchat'

urlpatterns = [
    path('', HomeView.as_view(), name = 'homepage'),
    path('login/', LoginView.as_view(template_name = 'dbchat/login.html'), name = 'login'),
    path('private_chat/<int:id>/', PrivateChatView.as_view(), name = 'private_chat'),
    path('check_username/<str:username>/', CheckUsernameView.as_view(), name = 'check_username'),
    path('signup/', SignUpView.as_view(), name = 'signup'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
]

