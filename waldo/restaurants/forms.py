from django import forms
from .models import Restaurant

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'postal_code', 'city']
from django import forms

class RestaurantSearchForm(forms.Form):
    name = forms.CharField(required=False, label="Nom")
    city = forms.CharField(required=False, label="Ville")
    postal_code = forms.CharField(required=False, label="Code postal")
