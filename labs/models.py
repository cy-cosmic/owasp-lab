from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from polls.models import Poll, Choice


# Create your models here.
class SandboxPoll(models.Model):
    original_poll = models.ForeignKey(
        Poll, null=True, blank=True, on_delete=models.CASCADE, related_name="sandbox_copies"
    )
    question = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    is_published = models.BooleanField(default=False)
    is_production = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_modified = models.BooleanField(default=False)
    session_id = models.CharField(max_length=64)

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse(
            'labs:sandbox_poll_detail',
            kwargs={
                'poll_id': self.id,
                'session_id': self.session_id
            }
        )


class SandboxChoice(models.Model):
    poll = models.ForeignKey(SandboxPoll, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


@receiver(post_save, sender=SandboxPoll)
def copy_choices_from_poll(sender, instance, created, **kwargs):
    if created and instance.original_poll:
        # Get all choices from the original Poll
        original_choices = Choice.objects.filter(poll=instance.original_poll)
        # Copy each choice into the sandbox
        for choice in original_choices:
            SandboxChoice.objects.create(
                poll=instance,
                choice_text=choice.choice_text,
                votes=0  # start fresh votes in sandbox
            )
