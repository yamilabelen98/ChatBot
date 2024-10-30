from django.db import models
from django.utils import timezone
from datetime import timedelta

class Conversation(models.Model):
    user_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def clean_old_conversations(cls):
        # Eliminar conversaciones más antiguas que 24 horas
        old_conversations = cls.objects.filter(
            created_at__lt=timezone.now() - timedelta(hours=24)
        )
        old_conversations.delete()    

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_bot = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']