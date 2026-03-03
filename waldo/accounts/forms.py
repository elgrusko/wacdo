from django import forms
from django.contrib.auth import get_user_model
from types_poste.models import TypePoste

User = get_user_model()

'''
This form : 
- is used to create and edit collaborators (users)
- includes a password field that is hashed when saved
- in edit mode, the password field is optional and if left empty, the current password is
    kept unchanged
- includes a search form to filter collaborators by username, first name, last name, email and unassigned status
- includes a form to filter affectations by position type and start date
'''
class CollaboratorCreationForm(forms.ModelForm):
    # PasswordInput widget to render the password field as a password input (with dots instead of characters)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'date_first_hired',
            'is_admin',
            'password',
        ]

    # In edit mode, password can be left empty to keep the current password.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # "instance" is the user being edited.
        # get the initial password hash to keep it if the password field is left empty in edit mode.
        self._initial_password_hash = self.instance.password if self.instance and self.instance.pk else None
        # Instance with PK means we are in edit mode, so we make the password field not required and add a help text to indicate that leaving it empty will keep the current password.
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            self.fields['password'].help_text = "Laissez vide pour conserver le mot de passe actuel."

    # Override save to hash a new password, or keep the existing hash in edit mode.
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)
        elif self._initial_password_hash:
            user.password = self._initial_password_hash

        if commit:
            user.save()
        return user

class CollaboratorSearchForm(forms.Form):
    username = forms.CharField(required=False, label="Nom d'utilisateur")
    first_name = forms.CharField(required=False, label="Prénom")
    last_name = forms.CharField(required=False, label="Nom de famille")
    email = forms.CharField(required=False, label="Email")
    unassigned_only = forms.BooleanField(required=False, label="Seulement les collaborateurs non affectés")


class CollaboratorAffectationFilterForm(forms.Form):
    position_type = forms.ModelChoiceField(
        # queryset to get all position types ordered by label
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
