from django.urls import path
from .views import create_affectation_for_restaurant, list_affectations

urlpatterns = [
    path("", list_affectations, name="affectation_list"),
    path("restaurants/<int:restaurant_pk>/create/", create_affectation_for_restaurant, name="affectation_create_for_restaurant"),
]
