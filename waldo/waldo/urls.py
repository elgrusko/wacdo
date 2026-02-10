"""waldo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # use an already built-in login view from django instead of creating our own
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # same for logout view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('protected/', account_views.protected_view, name='protected'),
    path('admin-only/', account_views.admin_only_view, name='admin-only'),
    path('types_poste/', include('types_poste.urls')),
    path('restaurants/', include('restaurants.urls')),
]
