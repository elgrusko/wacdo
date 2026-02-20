from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import admin_required
from restaurants.models import Restaurant
from .forms import AffectationCreateForm

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