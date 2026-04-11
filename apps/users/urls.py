from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("producer/", views.producer_panel, name="producer_panel"),
]
