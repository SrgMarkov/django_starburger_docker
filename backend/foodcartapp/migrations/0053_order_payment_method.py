# Generated by Django 3.2.15 on 2023-10-19 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0052_auto_20231019_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('OFFLINE', 'Оплата курьеру'), ('ONLINE', 'Оплачен на сайте')], db_index=True, default='OFFLINE', max_length=20, verbose_name='Способ оплаты'),
        ),
    ]
