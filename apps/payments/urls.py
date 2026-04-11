from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("status/", views.payment_status, name="status"),
]
