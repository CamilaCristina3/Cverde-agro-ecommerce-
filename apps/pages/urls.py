from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('politica-privacidade/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('termos/', views.TermsOfUseView.as_view(), name='terms_of_use'),
    path('politica-cookies/', views.CookiesPolicyView.as_view(), name='cookies_policy'),
]
