from django.core.management import BaseCommand

from users.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        email = str(input('Почта: '))
        phone = str(input('Номер телефона: '))
        first_name = str(input('Имя: '))
        last_name = str(input('Фамилия: '))
        while True:
            password1 = str(input('Пароль: '))
            password2 = str(input('Подтвердите пароль: '))
            if password1 == password2:
                password = password2
                break
            else:
                print('\nПароли не совпадают, попробуйте ещё раз.\n')

        user = User.objects.create(
            email=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            job_title='администратор',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password(password)
        user.save()
        print('\nПрофиль администратора создан.\n')