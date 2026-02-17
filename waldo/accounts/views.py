from django.shortcuts import render, redirect
from django.http import HttpResponse
from .decorators import admin_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import CollaboratorCreationForm, CollaboratorSearchForm
from .decorators import admin_required

User = get_user_model()

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
    # Initialize the search form with GET parameters (if any)
    form = CollaboratorSearchForm(request.GET)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')

        if username:
            # Use __icontains for case-insensitive partial matching
            collaborators = collaborators.filter(username__icontains=username)

        if first_name:
            collaborators = collaborators.filter(first_name__icontains=first_name)

        if last_name:
            collaborators = collaborators.filter(last_name__icontains=last_name)

        if email:
            collaborators = collaborators.filter(email__icontains=email)

    return render(
        request,
        'accounts/list_collaborators.html',
        {
            'collaborators': collaborators,
            'form': form
        }
    )

@admin_required
def detail_collaborator(request, collaborator_id):
    collaborator = User.objects.get(pk=collaborator_id)
    return render(request, 'accounts/detail_collaborator.html', {'collaborator': collaborator})