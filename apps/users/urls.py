"""
COVERDE - apps/users/urls.py
URLs de utilizadores (Portugal).
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Registo
    path('registar/', views.register, name='register'),
    path('register/', views.register),
    path('registar/consumidor/', views.register_client, name='register_consumer'),
    path('register/consumer/', views.register_client),
    path('registar/produtor/', views.register_producer, name='register_producer'),  # ← Produtor
    path('register/producer/', views.register_producer),

    # Ativação
    path('ativar/<uuid:token>/', views.activate_account, name='activate'),  # ← Portugal
    path('activate/<uuid:token>/', views.activate_account),

    # Autenticação
    path('entrar/', views.user_login, name='login'),
    path('login/', views.user_login),
    path('sair/', views.user_logout, name='logout'),
    path('logout/', views.user_logout),

    # Perfil
    path('perfil/', views.profile, name='profile'),
    path('profile/', views.profile),
    path('perfil/editar/', views.profile_edit, name='profile_edit'),
    path('profile/edit/', views.profile_edit),
    path('perfil/eliminar/', views.delete_account, name='delete_account'),
    path('profile/delete/', views.delete_account),
    path('perfil/moradas/adicionar/', views.add_address, name='add_address'),  # ← Portugal: moradas
    path('profile/addresses/add/', views.add_address),

    # Painel do produtor
    path('produtor/', views.producer_panel, name='producer_panel'),
    path('produtor/verificacao/', views.producer_verification, name='producer_verification'),
    path('produtor/produtos/', views.producer_products, name='producer_products'),
    path('produtor/produtos/novo/', views.product_create, name='product_create'),
    path('produtor/produtos/<uuid:product_id>/editar/', views.product_edit, name='product_edit'),
    path('produtor/produtos/<uuid:product_id>/eliminar/', views.product_delete, name='product_delete'),

    # Compatibilidade com templates legados
    path('produtos/', views.product_list_redirect, name='product_list'),

    # Recuperação de password
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]
