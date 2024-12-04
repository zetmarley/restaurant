from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    first_name = models.CharField(max_length=35, verbose_name='имя')
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    job_title = models.CharField(max_length=100, verbose_name='должность')
    phone = models.CharField(max_length=11, verbose_name='номер телефона', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'работник'
        verbose_name_plural = 'работники'
