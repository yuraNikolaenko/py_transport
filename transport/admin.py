from django.contrib import admin
from .models import Car, Driver, Route, Trip, RepairExpense, User
from django.utils.html import format_html
from django.urls import reverse


admin.site.register(User)
admin.site.register(Route)
admin.site.register(RepairExpense)

class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'number_plate', 'driver')
    search_fields = ('brand', 'model', 'number_plate')
    list_filter = ('status',)
    autocomplete_fields = ('driver',)  # Додає поле вибору водія

class DriverAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'contact', 'license_number')
    search_fields = ('full_name', 'license_number')

admin.site.register(Car, CarAdmin)
admin.site.register(Driver, DriverAdmin)


class TripAdmin(admin.ModelAdmin):
    list_display = ("date", "car", "driver", "get_distance", "fuel_consumed", "download_report")

    def get_distance(self, obj):
        """Возвращает пробег из связанного маршрута"""
        return obj.route.distance_km if obj.route else "—"

    get_distance.short_description = "Пробег (км)"  # Название столбца в админке

    def download_report(self, obj):
        url = reverse("trip_report") + f"?start_date={obj.date}&end_date={obj.date}"
        return format_html('<a href="{}" class="button">📄 PDF</a>', url)

    download_report.short_description = "Отчёт"

admin.site.register(Trip, TripAdmin)

