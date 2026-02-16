from django.urls import path
from .views import create_collaborator

urlpatterns = [
    path('create/', create_collaborator, name='collaborator_create'),
]
