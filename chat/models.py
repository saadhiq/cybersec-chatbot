from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatSession(models.Model):
    student    = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    summary    = models.TextField(blank=True)
    score      = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Session {self.id} - {self.student.username}"


class Message(models.Model):
    ROLE_CHOICES = [('user', 'User'), ('assistant', 'Assistant')]

    session   = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    role      = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.role}] {self.content[:50]}"