# Generated by Django 3.2.15 on 2023-10-20 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0054_order_cooking_restaurant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['status'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
    ]
