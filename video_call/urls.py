from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register_meeting, name="register_meeting"),
    path("join/", views.join_meeting, name="join_meeting"),
    path("room/<str:meeting_id>/", views.meeting_room, name="meeting_room"),
]
