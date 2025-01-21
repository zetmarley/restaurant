import datetime

from django import forms
from django.forms import HiddenInput

from config.settings import local_tz
from main.models import Booking, Table, Content


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
        client_email = cleaned_data.get('client_email')
        table = cleaned_data.get('table')
        time_from = cleaned_data.get('time_from')
        time_to = cleaned_data.get('time_to')

        if len(Booking.objects.filter(client_email=client_email)) > 2:
            raise forms.ValidationError("У вас уже есть 2 брони.")

        if time_from >= time_to:
            raise forms.ValidationError("Время начала бронирования должно быть раньше времени окончания.")

        if time_from <= datetime.datetime.now(tz=local_tz):
            raise forms.ValidationError("К сожалению, нельзя забронировать стол в прошлом времени.")

        if time_from > datetime.datetime.now(tz=local_tz) + datetime.timedelta(days=15):
            raise forms.ValidationError("Выберите время пораньше, пожалуйста.")

        if time_to - time_from > datetime.timedelta(hours=6):
            raise forms.ValidationError("К сожалению, нельзя забронировать стол на такой"
                                        "долгий промежуток времени.")

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
        fields = ('id', 'number', 'free', 'seats', 'is_vip')


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = '__all__'