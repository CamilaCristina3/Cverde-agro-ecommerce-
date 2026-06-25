# Authentication and User Management Views
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view - STUB"""
    return render(request, 'auth/login.html')


@require_http_methods(["GET", "POST"])
def register_view(request):
    """User registration view - STUB"""
    return render(request, 'auth/register.html')


@require_http_methods(["GET"])
def logout_view(request):
    """User logout view"""
    logout(request)
    return redirect('home')
