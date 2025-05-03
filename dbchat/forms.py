from django.forms import ModelForm
from .models import ChatMessage, Group


class ChatForm(ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']