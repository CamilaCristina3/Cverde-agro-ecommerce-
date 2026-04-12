from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("verify-email/<uuid:token>/", views.verify_email, name="verify_email"),
    path("two-factor/", views.two_factor_verify, name="two_factor_verify"),
    path("register/", views.register_choice, name="register"),
    path("register/consumer/", views.register_consumer, name="register_consumer"),
    path("register/producer/", views.register_producer, name="register_producer"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="profile_edit"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("producer/", views.producer_panel, name="producer_panel"),
    path("producer/verification/", views.producer_verification_request, name="producer_verification"),
    
    # Password reset views
    path("password-reset/", views.CustomPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", views.CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/", views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset/complete/", views.CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
