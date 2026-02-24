from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from accounts.decorators import admin_required
from .models import Affectation
from restaurants.models import Restaurant
from .forms import (
    AffectationCreateForm,
    AffectationSearchForm,
    CollaboratorAffectationCreateForm,
)

User = get_user_model()


@admin_required
def list_affectations(request):
    affectations = Affectation.objects.select_related(
        "collaborator",
        "restaurant",
        "position_type",
    )
    form = AffectationSearchForm(request.GET)

    if form.is_valid():
        position_type = form.cleaned_data.get("position_type")
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")
        city = form.cleaned_data.get("city")

        if position_type:
            affectations = affectations.filter(position_type=position_type)

        if start_date:
            affectations = affectations.filter(start_date=start_date)

        if end_date:
            affectations = affectations.filter(end_date=end_date)

        if city:
            affectations = affectations.filter(restaurant__city__icontains=city)

    return render(
        request,
        "affectations/list.html",
        {
            "affectations": affectations,
            "form": form,
        },
    )

@admin_required
def create_affectation_for_restaurant(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_pk)

    if request.method == "POST":
        form = AffectationCreateForm(request.POST, restaurant=restaurant)
        if form.is_valid():
            form.save()
            return redirect('detail_restaurant', restaurant_id=restaurant.id)
    else:
        form = AffectationCreateForm(restaurant=restaurant)

    return render(
        request,
        "affectations/create_for_restaurant.html",
        {"form": form, "restaurant": restaurant},
    )


@admin_required
def create_affectation_for_collaborator(request, collaborator_pk):
    collaborator = get_object_or_404(User, pk=collaborator_pk)

    if request.method == "POST":
        form = CollaboratorAffectationCreateForm(request.POST, collaborator=collaborator)
        if form.is_valid():
            form.save()
            return redirect("collaborator_detail", collaborator_id=collaborator.id)
    else:
        form = CollaboratorAffectationCreateForm(collaborator=collaborator)

    return render(
        request,
        "affectations/create_for_collaborator.html",
        {"form": form, "collaborator": collaborator},
    )
