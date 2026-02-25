from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone

from types_poste.models import TypePoste

from .models import Affectation

def _has_other_active_affectation(collaborator, exclude_pk=None):
    today = timezone.localdate()
    # get all affectations for the collaborator that are active
    queryset = Affectation.objects.filter(collaborator=collaborator).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=today)
    )
    # If exclude_pk is provided, we exclude that specific affectation from the check (useful when updating an existing affectation)
    if exclude_pk is not None:
        queryset = queryset.exclude(pk=exclude_pk)
    # simpl return bool (exists or not)
    return queryset.exists()


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
        today = timezone.localdate()
        # is_active is True if end_date is not provided (None) or if end_date is in the future (greater or equal to today)
        is_active = end_date is None or end_date >= today

        # Rule A : end_date must be after start_date (if end_date is provided)
        if start_date and end_date and end_date < start_date:
            raise ValidationError("La date de fin doit être postérieure ou égale à la date de début.")

        # Rule B : a collaborator cannot have more than one active affectation (end_date is null or in the future)
        if collaborator and is_active and _has_other_active_affectation(collaborator):
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

# Same validation rules as AffectationCreateForm, but without the restaurant since it's not created from the restaurant context but from the collaborator context.
class CollaboratorAffectationCreateForm(forms.ModelForm):
    class Meta:
        model = Affectation
        fields = ["restaurant", "position_type", "start_date", "end_date"]

    def __init__(self, *args, collaborator=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.collaborator = collaborator  # Contextual collaborator for this form

    def clean(self):
        cleaned = super().clean()
        start_date = cleaned.get("start_date")
        end_date = cleaned.get("end_date")
        today = timezone.localdate()
        is_active = end_date is None or end_date >= today

        # Rule A : end_date must be after start_date (if end_date is provided)
        if start_date and end_date and end_date < start_date:
            raise ValidationError("La date de fin doit être postérieure ou égale à la date de début.")

        # Rule B : a collaborator cannot have more than one active affectation
        if self.collaborator and is_active and _has_other_active_affectation(self.collaborator):
            raise ValidationError(
                "Ce collaborateur a déjà une affectation en cours. "
                "Clôture l’affectation actuelle avant d’en créer une nouvelle."
            )

        return cleaned

    # Override the save method to set the collaborator from the context
    def save(self, commit=True):
        obj = super().save(commit=False)
        if not self.collaborator:
            raise ValueError("Collaborateur manquant : ce formulaire doit être utilisé depuis un collaborateur.")
        obj.collaborator = self.collaborator
        if commit:
            obj.save()
        return obj


class AffectationSearchForm(forms.Form):
    # model choice field to get all position types ordered by label, with an empty option for "all"
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


class AffectationUpdateForm(forms.ModelForm):
    class Meta:
        model = Affectation
        fields = ["end_date"]
        widgets = {
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["end_date"].required = True
        # Keep end_date empty by default on GET to force an explicit closure date.
        if not self.is_bound and self.instance and self.instance.pk:
            self.initial["end_date"] = None

    def clean(self):
        cleaned = super().clean()
        end_date = cleaned.get("end_date")
        start_date = self.instance.start_date if self.instance else None

        if end_date and start_date and end_date < start_date:
            raise ValidationError("La date de fin doit être postérieure ou égale à la date de début.")

        return cleaned
