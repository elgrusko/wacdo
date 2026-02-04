from django.shortcuts import render
from django.http import HttpResponse
from .decorators import admin_required
from django.contrib.auth.decorators import login_required

@login_required
def protected_view(request):
    return HttpResponse("This is a protected view. You are logged in as: " + request.user.username)

@admin_required
def admin_only_view(request):
    return HttpResponse("This is an admin-only view. You have admin privileges.")