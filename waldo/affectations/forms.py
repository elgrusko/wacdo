from django import forms
from django.core.exceptions import ValidationError

from types_poste.models import TypePoste

from .models import Affectation

class AffectationCreateForm(forms.ModelForm):
    class Meta:
        model = Affectation
        fields = ["collaborator", "position_type", "start_date", "end_date"]

    def __init__(self, *args, restaurant=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.restaurant = restaurant  # Contextual restaurant for this form, must be provided when instantiating the form

    # Custom validation
    def clean(self):
        cleaned = super().clean()
        collaborator = cleaned.get("collaborator")
        start_date = cleaned.get("start_date")
        end_date = cleaned.get("end_date")

        # Rule A : end_date must be after start_date (if end_date is provided)
        if start_date and end_date and end_date < start_date:
            raise ValidationError("La date de fin doit être postérieure ou égale à la date de début.")

        # Rule B : a collaborator cannot have more than one active affectation (end_date is null or in the future)
        if collaborator:
            existing = Affectation.objects.filter(
                collaborator=collaborator,
                end_date__isnull=True,
            )

            if existing.exists():
                raise ValidationError(
                    "Ce collaborateur a déjà une affectation en cours. "
                    "Clôture l’affectation actuelle avant d’en créer une nouvelle."
                )

        return cleaned

    # Override the save method to set the restaurant from the context
    def save(self, commit=True):
        obj = super().save(commit=False)
        if not self.restaurant:
            raise ValueError("Restaurant manquant : ce formulaire doit être utilisé depuis un restaurant.")
        obj.restaurant = self.restaurant
        if commit:
            obj.save()
        return obj


class AffectationSearchForm(forms.Form):
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
    end_date = forms.DateField(
        required=False,
        label="Date de fin",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    city = forms.CharField(required=False, label="Ville")
