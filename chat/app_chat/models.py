from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Thread(models.Model):
    class Meta:
        verbose_name = 'thread'

    participants = models.ManyToManyField(User, related_name='threads')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.participants.count() > 2:
            raise ValidationError("A thread can't have more than 2 participants.")

    def save(self, *args, **kwargs):
        if self.pk:
            self.full_clean()
        super().save(*args, **kwargs)


class Message(models.Model):
    class Meta:
        verbose_name = 'message'

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
