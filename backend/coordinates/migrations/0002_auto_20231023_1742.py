# Generated by Django 3.2.15 on 2023-10-23 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordinates', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='addresscoordinates',
            options={'verbose_name': 'Адрес', 'verbose_name_plural': 'Адреса'},
        ),
        migrations.AlterField(
            model_name='addresscoordinates',
            name='address',
            field=models.CharField(max_length=100, null=True, verbose_name='Адрес'),
        ),
    ]
