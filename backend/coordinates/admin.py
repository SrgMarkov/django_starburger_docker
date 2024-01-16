from django.contrib import admin
from coordinates.models import AddressCoordinates


@admin.register(AddressCoordinates)
class Coordinates(admin.ModelAdmin):
    list_display = [
        'address',
    ]

