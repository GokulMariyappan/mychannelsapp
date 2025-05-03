from django.urls import path
from . import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'),
    path('login', auth.LoginView.as_view(template_name = 'mychatapp/login.html'), name = 'login')
]