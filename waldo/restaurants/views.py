from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone

from .forms import RestaurantForm, RestaurantSearchForm, RestaurantCollaboratorFilterForm
from .models import Restaurant
from accounts.decorators import admin_required

@admin_required
def restaurant_create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_restaurants')
    else:
        form = RestaurantForm()
    return render(request, 'restaurants/create.html', {'form': form})

@admin_required
def restaurant_list(request):
    # Get all restaurants (il all cases)
    restaurants = Restaurant.objects.all().order_by('name')
    # Initialize the search form with GET parameters (if any)
    form = RestaurantSearchForm(request.GET)

    if form.is_valid():
        name = form.cleaned_data.get('name')
        city = form.cleaned_data.get('city')
        postal_code = form.cleaned_data.get('postal_code')

        if name:
            #Use __icontains for case-insensitive partial matching
            restaurants = restaurants.filter(name__icontains=name)

        if city:
            restaurants = restaurants.filter(city__icontains=city)

        if postal_code:
            restaurants = restaurants.filter(postal_code__icontains=postal_code)

    return render(
        request,
        'restaurants/list.html',
        {
            'restaurants': restaurants,
            'form': form
        }
    )

@admin_required
def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    today = timezone.localdate()
    # - Get only affectations that are currently active (no end date or end date in the future).
    # - "select_related" to optimize queries. It will fetch the related collaborator and position_type in the same query.
    # - Q() stands for "Query" and is used to build complex queries with OR cnditions.
    active_affectations = restaurant.affectations.select_related(
        "collaborator",
        "position_type",
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=today)
    )
    filter_form = RestaurantCollaboratorFilterForm(request.GET)

    if filter_form.is_valid():
        position_type = filter_form.cleaned_data.get("position_type")
        start_date = filter_form.cleaned_data.get("start_date")

        if position_type:
            active_affectations = active_affectations.filter(position_type=position_type)

        if start_date:
            active_affectations = active_affectations.filter(start_date=start_date)

    return render(
        request,
        'restaurants/detail.html',
        {
            'restaurant': restaurant,
            'filter_form': filter_form,
            'active_affectations': active_affectations,
        },
    )

@admin_required
def restaurant_edit(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('detail_restaurant', restaurant_id=restaurant.id)
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'restaurants/edit.html', {'form': form, 'restaurant': restaurant})
