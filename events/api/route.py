from django.urls import path
from . import views

urlpatterns = [
    path('events', views.EventList.as_view()),
    path('attendances', views.AttendanceList.as_view()),
  
]