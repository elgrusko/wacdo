from django.urls import path
from .views import create_type_poste, list_type_poste, edit_type_poste, delete_type_poste

urlpatterns = [
    path('', list_type_poste, name='type_poste_list'),
    path('create/', create_type_poste, name='type_poste_create'),
    path('edit/<int:poste_id>/', edit_type_poste, name='type_poste_edit'),
    path('delete/<int:poste_id>/', delete_type_poste, name='type_poste_delete'),
]
