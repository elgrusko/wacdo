from django.shortcuts import render, redirect
from django.http import HttpResponse
from .decorators import admin_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import CollaboratorCreationForm
from .decorators import admin_required

User = get_user_model()

@login_required
def protected_view(request):
    return HttpResponse("This is a protected view. You are logged in as: " + request.user.username)

@admin_required
def admin_only_view(request):
    return HttpResponse("This is an admin-only view. You have admin privileges.")

@login_required
def home(request): 
    return render(request, 'home.html')

@admin_required
def create_collaborator(request):
    if request.method == "POST":
        form = CollaboratorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CollaboratorCreationForm()

    return render(
        request,
        'accounts/create_collaborator.html',
        {'form': form}
    )

@admin_required
def list_collaborators(request):
    collaborators = User.objects.all().order_by('username')
    return render(
        request,
        'accounts/list_collaborators.html',
        {'collaborators': collaborators}
    )