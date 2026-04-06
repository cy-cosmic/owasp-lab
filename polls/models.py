from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


def get_demo_user():
    return User.objects.get(username="demo_user").id


# Create your models here.
class Poll(models.Model):
    question = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    is_published = models.BooleanField(default=False)
    is_production = models.BooleanField(default=True)

    # Self-reference for sandbox linking
    original_poll = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.choice_text} ({self.votes})"
