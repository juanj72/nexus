from django.contrib import admin
from .models import Event, Attendance
from leaflet.admin import LeafletGeoAdmin
# Register your models here.

@admin.register(Event)
class EventAdmin(LeafletGeoAdmin):
    class Media:
        js = ('js/geolocation.js',)  



@admin.register(Attendance)
class AttendanceAdmin(LeafletGeoAdmin):
    pass