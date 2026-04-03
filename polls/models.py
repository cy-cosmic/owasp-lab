from django.db import models
from django.utils import timezone


# Create your models here.
class Poll(models.Model):
    question = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.choice_text} ({self.votes})"