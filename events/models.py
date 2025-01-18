from django.db import models
from ..user.models import User


# Create your models here.

#status choices


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    event_manager = models.ForeignKey(User, on_delete=models.CASCADE)
    status = 