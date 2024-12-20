import datetime
import json
import os
from time import tzname
from pathlib import Path
import pytz
from dateutil import tz
from django.conf import settings
from django.core.mail import send_mail

from config.settings import local_tz, BASE_DIR
from main.models import Booking, Table
from celery import shared_task

# @shared_task
# def send_mailing(instance, model):
#     if model == 'Course':
#         subscriptions = Subscription.objects.filter(course_id=instance.pk)
#         email_list = []
#         for i in subscriptions:
#             email = i.user.email
#             email_list.append(email)
#
#         send_mail(
#                 subject=f'Курс {instance.title} обновлён',
#                 message=f'Курс {instance.title} обновлён\nПосмотрите что добавили нового',
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=email_list
#         )
#         return Response(data={'message': 'Подписчики уведомлены'})
#
#     elif model == 'Lesson':
#         subscriptions = Subscription.objects.filter(lesson_id=instance.pk)
#         email_list = []
#         for i in subscriptions:
#             email = i.user.email
#             email_list.append(email)
#
#         send_mail(
#             subject=f'Урок {instance.title} обновлён',
#             message=f'Урок {instance.title} обновлён\nПосмотрите что добавили нового',
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=email_list
#         )
#         return Response(data={'message': 'Подписчики уведомлены'})

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
            print('aboba')
            table.save()

