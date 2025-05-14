import base64
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .models import ChatMessage, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ChatForm
from django.contrib.auth.models import User
import json 
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.core.files.base import ContentFile

class HomeView(LoginRequiredMixin, View):
    users = User.objects.all()
    def get(self,  request):
        form = ChatForm()
        try:
            group = Group.objects.get(name = 'public_chat')
        except:
            group = Group.objects.create(name = 'public_chat')
        messages = ChatMessage.objects.filter(group = group)
        return render(request , "dbchat/public_chat.html", {'messages' : messages, 'user' : request.user, 'form' : form, 'users' : self.users})
    
    def post(self, request):
        print('im called im the POSTTT')
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
        return f'{id2}_{id1}'
    else:
        return f'{id1}_{id2}'

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
    
class PublicChatConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope['user'].is_authenticated:
            self.room_group_name = 'public_chat'
            async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
            self.accept()
            self.send(text_data = json.dumps({'message' : 'websocket connected(public chat)','type' : 'init'}))
        else:
            self.close()
        
    def receive(self, text_data=None):
        message = json.loads(text_data)
        received_message = message['message']
        fileObject = None
        image = None
        if message['file']:
            data = base64.b64decode(message['fileData'])
            fileObject = ContentFile(data, name = message['filename'])
            if message['filetype'].startswith('image'):
                image = fileObject
                fileObject = None
        message = ChatMessage.objects.create(user = self.scope['user'], group = Group.objects.get(name = 'public_chat'), message = received_message, image = image, files = fileObject)
        print(f"received message : {received_message} from {self.scope['user']}")
        async_to_sync(self.channel_layer.group_send)(self.room_group_name,{'type':'chat_message', 'message' : message, 'sender' : self.channel_name, 'username' : self.scope['user'].username})

    def chat_message(self, event):
        data = event['message']
        message = None
        fileURL = None
        image = None
        if data.message:
            message = data.message
        if data.files:
            fileURL = data.files.url[7:]
        if data.image:
            image = data.image.url[7:]
        if(event['sender'] == self.channel_name):
            self.send(text_data = json.dumps({'sender' : 'Me', 'type': 'websocket_response', 'message' : message, 'file' : fileURL, 'image' : image}))
            print(f"sent by {self.scope['user']}")
            return
        self.send(json.dumps({'sender' : event['username'], 'type': 'websocket_response', 'message' : message, 'file' : fileURL, 'image' : image}))
        print(f"sent by {self.scope['user']}")

class PrivateChatConsumer(WebsocketConsumer):
    second_user = None
    def connect(self):
        if(self.scope['user'].is_authenticated):
            sid = self.scope['url_route']['kwargs']['id']
            room_group_name = generate_group_name(self.scope['user'].id, sid)
            self.room_group_name = room_group_name
            async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
            self.second_user = User.objects.get(id = sid)
            self.accept()
            self.send(json.dumps({'message' : f'sid: {sid}, {room_group_name}', 'type' : 'check_connection'}))
        else:
            self.close()
    
    def receive(self, text_data = None):
        clientData = json.loads(text_data)
        received_message = clientData['message']
        fileBool = clientData['file']
        fileObject = None
        image = None
        if(fileBool):
            data = clientData.get('fileData')
            fileData = base64.b64decode(data)
            fileObject = ContentFile(fileData, name = clientData['filename'])
        
        if(clientData.get('filetype')):
            if(clientData.get('filetype').startswith('image')):
                image = fileObject
                fileObject = None
        try:
            group = Group.objects.get(name = generate_group_name(self.scope['user'].id, self.second_user.id))
        except:
            group = Group.objects.create(name = generate_group_name(self.scope['user'].id, self.second_user.id))
        message = ChatMessage.objects.create(user = self.scope['user'], group = group, message = received_message, image = image, files = fileObject)
        print(f"{self.scope['user']} sent {received_message} to {self.second_user}")
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'message' : message,
                'sender' : self.channel_name,
                'username' : self.scope['user'].username
            }
        )

    def chat_message(self, event):
        message = None
        fileURL = None
        image = None
        if event['message'].message:
            message = event['message'].message
        if event['message'].files:
            fileURL = event['message'].files.url[7:]
        if event['message'].image:
            image = event['message'].image.url[7:]

        if(event['sender'] == self.channel_name):
            self.send(text_data = json.dumps({'sender': 'Me', 'type' : 'websocket_response', 'message' : message, 'file' : fileURL, 'image' : image}))
            return
        self.send(text_data = json.dumps({'sender': event['username'], 'type' : 'websocket_response', 'message' : message, 'file' : fileURL, 'image' : image}))

