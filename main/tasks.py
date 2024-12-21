import datetime
import json
import pytz
from dateutil import tz
from django.conf import settings
from django.core.mail import send_mail
from config.settings import local_tz, BASE_DIR
from main.models import Booking, Table
from celery import shared_task

@shared_task
def email_notification():
    booking_list = Booking.objects.filter(is_notified=False)

    if booking_list.exists():
        for booking in booking_list:
            time_from = booking.time_from.replace(tzinfo=None)
            if time_from - datetime.datetime.now(tz=None) <= datetime.timedelta(hours=1):
                time_from_tz = booking.time_from.astimezone()
                time_to_tz = booking.time_to.astimezone()

                send_mail(
                    subject=f'До начала бронирования остался час!',
                    message=f'Ваша бронь:\nСтол №{booking.table.pk}\nC {time_from_tz.hour}:'
                            f'{time_from_tz.minute} До {time_to_tz.hour}:{time_to_tz.minute}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[booking.client_email]
                )
                booking.is_notified = True
                booking.save()

@shared_task
def check_bookings():
    booking_list = Booking.objects.all()
    time_now = datetime.datetime.now(tz.gettz(settings.TIME_ZONE))
    table_list = Table.objects.all()
    for booking in booking_list:

        if booking.time_from <= time_now <= booking.time_to and booking.table.free == True:
            table = booking.table
            table.free = False
            table.save()

        if booking.time_from < time_now > booking.time_to:
            table = booking.table
            table.free = True
            table.save()

            time_from = booking.time_from
            time_from = str(time_from.replace(tzinfo=pytz.utc).astimezone(local_tz))[0:-6]

            time_to = booking.time_to
            time_to = str(time_to.replace(tzinfo=pytz.utc).astimezone(local_tz))[0:-6]

            booking_dict = {
                'id': booking.id,
                'table_id': booking.table.id,
                'time_from': time_from,
                'time_to': time_to,
                'client_email': booking.client_email,
                'client_name': booking.client_name,
                'client_phone': booking.client_phone
            }

            file = BASE_DIR / 'logs' / 'bookings' / f'{booking.id} {time_from}.txt'

            with open(file, 'w') as f:
                f.write(json.dumps(booking_dict))
            booking.delete()

    for table in table_list:
        if not Booking.objects.filter(table=table).exists() and table.free == False:
            table.free = True
            table.save()

