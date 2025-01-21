from django.urls import path
from user.api import views

urlpatterns = [
    path('list/', views.UserView.as_view()),
]