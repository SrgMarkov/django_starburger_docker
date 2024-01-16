from rest_framework.serializers import ModelSerializer
from phonenumber_field.serializerfields import PhoneNumberField

from .models import Order, OrderList, Product


class OrderListSerializer(ModelSerializer):
    class Meta:
        model = OrderList
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderListSerializer(many=True, allow_empty=False, write_only=True)
    phonenumber = PhoneNumberField()
    
    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product in products:
            price = product['product'].price * product['quantity']
            OrderList.objects.create(
                order=order,
                product=product['product'],
                quantity=product['quantity'],
                price=price)
        return order

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address',
                  'products']
