from django import forms
from .models import TypePoste

class TypePosteForm(forms.ModelForm):
    class Meta:
        model = TypePoste
        fields = ['label']

    ''' 
        this function is automatically called (because of his prefix 'clean_') when form is validated, it allows us to clean the label field before saving it to the database
        note that we also clean the label field in the model's save method, this is to ensure that the label is always cleaned regardless of how the form is submitted (e.g. through admin interface or directly through the model)
    '''
    def clean_label(self):
        label = self.cleaned_data['label']
        return label.strip().title()