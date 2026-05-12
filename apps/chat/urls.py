from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chat_index, name="index"),
    path("assistant/", views.chat_assistant, name="assistant"),
    path("rooms/create/", views.chat_create_room, name="create_room"),
    path("rooms/<slug:room_name>/", views.chat_room, name="room"),
]

