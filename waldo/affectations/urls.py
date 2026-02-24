from django.urls import path
from .views import (
    create_affectation_for_restaurant,
    create_affectation_for_collaborator,
    list_affectations,
)

urlpatterns = [
    path("", list_affectations, name="affectation_list"),
    path("restaurants/<int:restaurant_pk>/create/", create_affectation_for_restaurant, name="affectation_create_for_restaurant"),
    path("collaborators/<int:collaborator_pk>/create/", create_affectation_for_collaborator, name="affectation_create_for_collaborator"),
]
