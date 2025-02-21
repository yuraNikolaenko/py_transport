from django.contrib import admin
from .models import Car, Driver, Route, Trip, RepairExpense, User

admin.site.register(User)
admin.site.register(Car)
admin.site.register(Driver)
admin.site.register(Route)
admin.site.register(Trip)
admin.site.register(RepairExpense)
