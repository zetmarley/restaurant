from django import forms

from main.models import Booking


class BookingForm(forms.ModelForm):

    # def clean_description(self):
    #     for i in [self.cleaned_data['name'], self.cleaned_data['description']]:
    #         cleaned_data = i
    #         print(self.cleaned_data)
    #         if len(cleaned_data) < 3:
    #             raise forms.ValidationError('Название и описание продукта должно быть больше 3 символов')
    #         elif cleaned_data in ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']:
    #             raise forms.ValidationError('Название или описание продукта имеет недопустимые слова')

    class Meta:
        model = Booking
        fields = ('table', 'time_from', 'time_to', 'client_email', 'client_name', 'client_phone',)