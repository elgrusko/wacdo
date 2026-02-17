from django.urls import path
from .views import create_collaborator, list_collaborators, detail_collaborator

urlpatterns = [
    path('create/', create_collaborator, name='collaborator_create'),
    path('<int:collaborator_id>/', detail_collaborator, name='collaborator_detail'),
    path('', list_collaborators, name='collaborator_list'),
]
