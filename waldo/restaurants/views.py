from django.shortcuts import render, redirect, get_object_or_404
from .forms import RestaurantForm
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
    restaurants = Restaurant.objects.order_by('name')
    return render(request, 'restaurants/list.html', {'restaurants': restaurants})

@admin_required
def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'restaurants/detail.html', {'restaurant': restaurant})