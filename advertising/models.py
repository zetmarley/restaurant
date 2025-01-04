from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Subscribers(models.Model):
    """Модель стола"""

    email = models.EmailField(verbose_name='почта', **NULLABLE)
    phone = models.CharField(max_length=11, verbose_name='телефон', **NULLABLE)
    name = models.CharField(max_length=50, verbose_name='имя', **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.phone} {self.email}'

    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'подписчики'

