from rest_framework import serializers
from events.models import Event, Attendance
from rest_framework_gis.serializers import GeoModelSerializer
from django.contrib.gis.geos import Point


class EventSerializer(GeoModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        geo_field = 'location'

    def create(self, validated_data):
        # Convertir el campo 'location' a un objeto Point
        location_data = validated_data.get('location')
        if isinstance(location_data, dict) and location_data.get('type') == 'Point':
            validated_data['location'] = Point(*location_data['coordinates'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Convertir el campo 'location' a un objeto Point
        location_data = validated_data.get('location')
        if isinstance(location_data, dict) and location_data.get('type') == 'Point':
            validated_data['location'] = Point(*location_data['coordinates'])
        return super().update(instance, validated_data)

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'