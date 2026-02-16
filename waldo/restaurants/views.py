from django.shortcuts import render, redirect, get_object_or_404
from .forms import RestaurantForm, RestaurantSearchForm
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
    return render(request, 'restaurants/detail.html', {'restaurant': restaurant})

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