import datetime

from django.db import models
from django.utils import timezone


class AddressCoordinates(models.Model):
    address = models.CharField(
        verbose_name='Адрес',
        max_length=100,
        unique=True,
    )
    lon = models.FloatField(
        verbose_name='Долгота',
        null=True,
        blank=True,
    )
    lat = models.FloatField(
        verbose_name='Широта',
        null=True,
        blank=True,
    )
    coordinates_date = models.DateField(
        verbose_name='Дата запроса координат',
        default=timezone.now,
    )

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
