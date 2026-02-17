from django.urls import path
from .views import create_collaborator, list_collaborators

urlpatterns = [
    path('create/', create_collaborator, name='collaborator_create'),
    path('', list_collaborators, name='collaborator_list'),
]
