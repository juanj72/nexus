from django.urls import path
from . import views

urlpatterns = [
    path('event_list/', views.EventList.as_view()),
  
]