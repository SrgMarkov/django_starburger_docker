from django.db import models
from django.db.models import Sum
from django.core.validators import MinValueValidator
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=400,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def calculate_price(self):
        return self.annotate(price=Sum('list__price'))


class OrderList(models.Model):
    order = models.ForeignKey(
        'Order',
        verbose_name='Заказ',
        related_name='list',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'Product',
        verbose_name='Товар',
        related_name='in_order',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        'Количество'
    )
    price = models.DecimalField(
        'Стоимость',
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0, message='Цена не может быть отрицательной')]
    )

    class Meta:
        verbose_name = 'Состав заказа'
        verbose_name_plural = 'Состав заказа'


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('NEW', 'Новый'),
        ('COOK', 'Приготовление'),
        ('DELIVERY', 'Доставка'),
        ('READY', 'Исполнен'),
    ]
    PAYMENT_METHODS = [
        ('OFFLINE', 'Оплата курьеру'),
        ('ONLINE', 'Оплачен на сайте'),
        ('NOT_SET', 'Не задано')
    ]
    status = models.CharField(
        'Статус заказа',
        max_length=10,
        choices=ORDER_STATUS_CHOICES,
        default='NEW',
        db_index=True
    )
    firstname = models.CharField(
        'Имя',
        max_length=30
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=30
    )
    phonenumber = PhoneNumberField(
        'телефон'
    )
    address = models.CharField(
        'Адрес',
        max_length=200)
    comment = models.TextField(
        'Комментарий к заказу',
        max_length=400,
        blank=True,
    )
    registered_at = models.DateTimeField(
        'Время регистрации заказа',
        default=timezone.now,
        db_index=True
    )
    call_at = models.DateTimeField(
        'Время звонка клиенту',
        blank=True,
        null=True,
        db_index=True
    )
    delivered_at = models.DateTimeField(
        'Время доставки заказа',
        blank=True,
        null=True,
        db_index=True
    )
    payment_method = models.CharField(
        'Способ оплаты',
        max_length=20,
        choices=PAYMENT_METHODS,
        default='NOT_SET',
        db_index=True
    )
    cooking_restaurant = models.ForeignKey(
        'Restaurant',
        verbose_name='Какой ресторан готовит',
        related_name='order',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    objects = OrderQuerySet.as_manager()

    class Meta:
        ordering = ['status']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname} - {self.address}'
