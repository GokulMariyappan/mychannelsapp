from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    message = models.TextField(null= True, blank=True)
    image = models.ImageField(upload_to="", blank = True, null = True)
    files = models.FileField(upload_to = '', blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
