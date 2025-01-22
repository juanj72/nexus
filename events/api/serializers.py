from rest_framework import serializers
from events.models import Event, Attendance


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'  

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'