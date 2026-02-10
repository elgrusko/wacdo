from django.urls import path
from .views import restaurant_create, restaurant_list

urlpatterns = [
    path('create/', restaurant_create, name='create_restaurant'),
    path('', restaurant_list, name='list_restaurants'),
]
