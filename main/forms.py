from django import forms
from django.forms import HiddenInput

from main.models import Booking, Table


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ('table', 'time_from', 'time_to', 'client_email', 'client_name', 'client_phone', 'is_notified')
        widgets = {
            'time_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'time_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        time_from = cleaned_data.get('time_from')
        time_to = cleaned_data.get('time_to')

        if time_from >= time_to:
            raise forms.ValidationError("Время начала бронирования должно быть раньше времени окончания.")

        overlapping_bookings = Booking.objects.filter(
            table=table,
            time_from__lt=time_to,  # Начало существующего бронирования раньше конца нового
            time_to__gt=time_from  # Конец существующего бронирования позже начала нового
        )

        if overlapping_bookings.exists():
            raise forms.ValidationError("Данное бронирование пересекается с уже существующим. "
                                        "Выберите другое время пожалуйста")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['is_notified'].widget = HiddenInput()


class BookingUpdateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('table', 'time_from', 'time_to', 'client_email', 'client_name', 'client_phone', 'is_notified')
        widgets = {
            'time_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'time_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        time_from = cleaned_data.get('time_from')
        time_to = cleaned_data.get('time_to')

        if time_from >= time_to:
            raise forms.ValidationError("Время начала бронирования должно быть раньше времени окончания.")

        return cleaned_data


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ('id', 'free', 'seats', 'is_vip')
