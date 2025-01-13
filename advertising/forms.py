from django import forms
from advertising.models import Letters


class LettersForm(forms.ModelForm):
    class Meta:
        model = Letters
        fields = '__all__'