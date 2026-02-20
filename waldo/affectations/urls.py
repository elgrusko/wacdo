from django.urls import path
from .views import create_affectation_for_restaurant

urlpatterns = [
    path("restaurants/<int:restaurant_pk>/create/", create_affectation_for_restaurant, name="affectation_create_for_restaurant"),
]