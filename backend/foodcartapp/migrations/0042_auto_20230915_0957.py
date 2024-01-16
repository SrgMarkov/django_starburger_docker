# Generated by Django 3.2.15 on 2023-09-15 09:57

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0041_auto_20230915_0737'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='count',
            new_name='quantity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='in_order', to='foodcartapp.product', verbose_name='Товар'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=200, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='телефон'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='foodcartapp.customer', verbose_name='Заказчик'),
        ),
    ]