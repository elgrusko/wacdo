from django.urls import path
from .views import restaurant_create, restaurant_list, restaurant_detail, restaurant_edit

urlpatterns = [
    path('create/', restaurant_create, name='create_restaurant'),
    path('', restaurant_list, name='list_restaurants'),
    path('<int:restaurant_id>/', restaurant_detail, name='detail_restaurant'),
    path('<int:restaurant_id>/edit/', restaurant_edit, name='edit_restaurant'),
]
