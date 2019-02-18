from django import forms

from .models import Concept


class ConceptForm(forms.ModelForm):
    name = forms.CharField(label='名词', required=True, widget=forms.TextInput(
        attrs={'value': "", 'size': "30", 'maxlength': "245", 'aria-required': 'true'}))
    description = forms.EmailField(label='解释', required=True)

    class Meta:
        model = Concept
        fields = ['name', 'description']
