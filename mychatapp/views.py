from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'mychatapp/index.html', context={})