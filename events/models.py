from django.db import models
from user.models import User
from django.contrib.gis.db import models

# Create your models here.

#status choices
STATUS_EVENT = [
    ('active', 'active'),
    ('inactive', 'inactive'),
    ('cancelled', 'cancelled'),
    ('ended', 'ended')
    ]


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.PointField(srid=4326,null=True,blank=True)
    description = models.TextField()
    event_manager = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_EVENT,default='active')
    class Meta:
        db_table = 'event'


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField()
    entry_time = models.DateTimeField(null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    location_attendance = models.PointField(srid=4326,null=True,blank=True)
    type_data = models.CharField(max_length=255, null=True, blank=True)
    

    class Meta:
        unique_together = ('user', 'event')
        db_table = 'attendance'