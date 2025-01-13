from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Subscribers(models.Model):
    """Модель стола"""

    email = models.EmailField(verbose_name='почта', **NULLABLE)
    phone = models.CharField(max_length=11, verbose_name='телефон', **NULLABLE)
    name = models.CharField(max_length=50, verbose_name='имя', **NULLABLE)

    def __str__(self):
        return f'{str(self.name).title()} {self.phone}'

    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'подписчики'


class Letters(models.Model):
    subject = models.CharField(max_length=50, verbose_name='заголовок')
    message = models.TextField(verbose_name='сообщение')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'письмо {self.subject}'

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'