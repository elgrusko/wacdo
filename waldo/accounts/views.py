from django.shortcuts import render, redirect, get_object_or_404
from .decorators import admin_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from .forms import (
    CollaboratorCreationForm,
    CollaboratorSearchForm,
    CollaboratorAffectationFilterForm,
)

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
        unassigned_only = form.cleaned_data.get('unassigned_only')

        if username:
            # Use __icontains for case-insensitive partial matching
            collaborators = collaborators.filter(username__icontains=username)

        if first_name:
            collaborators = collaborators.filter(first_name__icontains=first_name)

        if last_name:
            collaborators = collaborators.filter(last_name__icontains=last_name)

        if email:
            collaborators = collaborators.filter(email__icontains=email)

        if unassigned_only:
            collaborators = collaborators.filter(affectations__isnull=True)

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
    collaborator = get_object_or_404(User, pk=collaborator_id)
    affectations = collaborator.affectations.select_related(
        "restaurant",
        "position_type",
    )
    filter_form = CollaboratorAffectationFilterForm(request.GET)

    if filter_form.is_valid():
        position_type = filter_form.cleaned_data.get("position_type")
        start_date = filter_form.cleaned_data.get("start_date")

        if position_type:
            affectations = affectations.filter(position_type=position_type)

        if start_date:
            affectations = affectations.filter(start_date=start_date)

    today = timezone.localdate()
    # Get only affectations that are currently active (no end date or end date in the future)
    active_affectations = affectations.filter(
        Q(end_date__isnull=True) | Q(end_date__gte=today)
    )

    # Get affectations that have ended in the past (end date before today)
    affectation_history = affectations.filter(end_date__lt=today)

    return render(
        request,
        'accounts/detail_collaborator.html',
        {
            'collaborator': collaborator,
            'filter_form': filter_form,
            'active_affectations': active_affectations,
            'affectation_history': affectation_history,
        },
    )

@admin_required
def edit_collaborator(request, collaborator_id):
    collaborator = User.objects.get(pk=collaborator_id)
    if request.method == "POST":
        form = CollaboratorCreationForm(request.POST, instance=collaborator)
        if form.is_valid():
            form.save()
            return redirect('collaborator_detail', collaborator_id=collaborator.id)
    else:
        form = CollaboratorCreationForm(instance=collaborator)

    return render(
        request,
        'accounts/edit_collaborator.html',
        {'form': form, 'collaborator': collaborator}
    )
