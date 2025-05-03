from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .models import ChatMessage, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ChatForm
from django.contrib.auth.models import User
# Create your views here.

class HomeView(LoginRequiredMixin, View):
    users = User.objects.all()
    def get(self,  request):
        form = ChatForm()
        messages = ChatMessage.objects.filter(group = Group.objects.get(name = 'public_chat'))
        return render(request , "dbchat/public_chat.html", {'messages' : messages, 'user' : request.user, 'form' : form, 'users' : self.users})
    
    def post(self, request):
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.save(commit = False)
            message.user  = request.user
            message.group = Group.objects.get(name = 'public_chat')
            message.save()
            return HttpResponseRedirect(request.path)
        else:
            messages = ChatMessage.objects.filter(group = Group.objects.get(name = 'public_chat'))
            error = 'some error occured in sending the message!!'
            return render(request , "dbchat/public_chat.html", {'error' : error, 'messages' : messages, 'user' : request.user, 'form' : form, 'users' : self.users})
        

def generate_group_name(id1, id2):
    if(id1 > id2):
        return f'{id2},{id1}'
    else:
        return f'{id1},{id2}'

class PrivateChatView(LoginRequiredMixin, View):
    def get(self, request, id):
        form = ChatForm()
        second_user = User.objects.get(id = id)
        try:
            group = Group.objects.get(name = generate_group_name(request.user.id, second_user.id))
        except:
            group = Group.objects.create(name = generate_group_name(request.user.id, second_user.id))
           
        messages = ChatMessage.objects.filter(group = group)
        return render(request, 'dbchat/private_chat.html', {'second_user' : second_user, 'messages' : messages, 'user' : request.user, 'form' : form})
    
    def post(self, request, id):
        form = ChatForm(request.POST)
        second_user = User.objects.get(id = id)
        if form.is_valid():
            message = form.save(commit = False)
            message.user = request.user
            message.group = Group.objects.get(name = generate_group_name(request.user.id, second_user.id))
            message.save()
            return HttpResponseRedirect(request.path)
        group = Group.objects.get(name = generate_group_name(request.user.id, second_user.id))
        messages = ChatMessage.objects.filter(group = group)
        error = 'Something went wrong!'
        return render(request, 'dbchat/private_chat.html', {'error' : error, 'second_user' : second_user, 'messages' : messages, 'user' : request.user, 'form' : form})