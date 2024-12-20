import datetime

from dateutil import tz
from django import forms
from django.conf import settings
from django.core.mail import send_mail

from main.models import Booking


class BookingForm(forms.ModelForm):


    class Meta:
        model = Booking
        fields = ('table', 'time_from', 'time_to', 'client_email', 'client_name', 'client_phone')
        widgets = {
            'time_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'time_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        client_email = cleaned_data.get('email')
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
        time_from = time_from.replace(tzinfo=None)
        print(time_from)
        print(time_from - datetime.datetime.now(tz=None))

        if overlapping_bookings.exists():
            raise forms.ValidationError("Данное бронирование пересекается с уже существующим. Выберите другое время пожалуйста")

        send_mail(
            subject=f'Вы забронировали стол!',
            message=f'Вы забронировали стол №{table.pk} {time_from.day} {time_from.hour}:{time_from.minute} До {time_to.hour}:{time_to.minute}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client_email]
        )


        if time_from - datetime.datetime.now(tz=None) <= datetime.timedelta(hours=1):
            cleaned_data['is_notified'] = True


        return cleaned_data