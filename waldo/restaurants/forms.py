from django import forms
from .models import Restaurant
from types_poste.models import TypePoste

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'postal_code', 'city']


class RestaurantSearchForm(forms.Form):
    name = forms.CharField(required=False, label="Nom")
    city = forms.CharField(required=False, label="Ville")
    postal_code = forms.CharField(required=False, label="Code postal")


class RestaurantCollaboratorFilterForm(forms.Form):
    position_type = forms.ModelChoiceField(
        queryset=TypePoste.objects.order_by("label"),
        required=False,
        label="Type de poste",
        empty_label="Tous les postes",
    )
    start_date = forms.DateField(
        required=False,
        label="Date de début",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
