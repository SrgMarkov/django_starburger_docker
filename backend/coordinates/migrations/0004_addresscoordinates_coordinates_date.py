# Generated by Django 3.2.15 on 2023-10-25 07:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordinates', '0003_auto_20231023_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresscoordinates',
            name='coordinates_date',
            field=models.DateField(default=datetime.date(2023, 10, 25), verbose_name='Дата запроса координат'),
        ),
    ]
