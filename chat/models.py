from django.db import models
from accounts.models import UserProfile
from matching.models import Match

class Conversation(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='conversation')
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='chat_files/', null=True, blank=True)
    reaction = models.CharField(max_length=10, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
