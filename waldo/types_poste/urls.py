from django.urls import path
from .views import create_type_poste, list_type_poste

urlpatterns = [
    path('', list_type_poste, name='type_poste_list'),
    path('create/', create_type_poste, name='type_poste_create'),
]
