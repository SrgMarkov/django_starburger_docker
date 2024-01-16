import datetime

import requests
from geopy import distance
from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

from coordinates.models import AddressCoordinates
from foodcartapp.models import Product, Restaurant, Order
from star_burger.settings import yandex_api_key

COORDINATE_UPDATE_RATE = 30


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability
                        for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False)
                                for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability':
            products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_or_create_coordinates(address):
    address, created = AddressCoordinates.objects.get_or_create(address=address)
    coordinates_request_date_delta = datetime.date.today() - address.coordinates_date
    if not created and address.lon and address.lat \
        and coordinates_request_date_delta.days < COORDINATE_UPDATE_RATE:
        return address.lon, address.lat
    else:
        coordinates = fetch_coordinates(yandex_api_key, address)
        if coordinates: #если запрос координат вернет  None - в панели менеджера отобразится ошибка определения координат
            address.lat = coordinates[0]
            address.lon = coordinates[1]
            address.coordinates_date = datetime.date.today()
            address.save()
            return address.lon, address.lat
        else:
            return None


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    orders = []
    for order in Order.objects.calculate_price().prefetch_related('list__product__menu_items'):
        restaurants_with_products = []
        for position in order.list.all():
            restaurants_with_products.append(set(menu_item.restaurant
                                                 for menu_item in position.product.menu_items.all()
                                                 if menu_item.availability))
        available = set.intersection(*restaurants_with_products)
        available_restaurants = {restaurant.name: restaurant.address for restaurant in available}

        order_coordinates = get_or_create_coordinates(order.address)
        if not order_coordinates:
            available_restaurants = 'Ошибка определения координат'
        else:
            for name, address in available_restaurants.items():
                restaurant_coordinates = get_or_create_coordinates(address)
                distance_to_restaurant = distance.distance(order_coordinates, restaurant_coordinates).km
                rounded_distance_to_restaurant = round(distance_to_restaurant, 2)
                available_restaurants[name] = rounded_distance_to_restaurant

        order_details = {'id': order.id,
                         'show': False if order.status == 'READY' else True,
                         'status_display': order.get_status_display(),
                         'payment_method': order.get_payment_method_display(),
                         'price': order.price,
                         'customer': f'{order.firstname} {order.lastname}',
                         'phone': order.phonenumber,
                         'address': order.address,
                         'comment': order.comment,
                         'available_restaurants': available_restaurants,
                         'cooking_restaurant': order.cooking_restaurant}
        orders.append(order_details)
    return render(request, template_name='order_items.html', context={
        'order_items': orders,
    })
