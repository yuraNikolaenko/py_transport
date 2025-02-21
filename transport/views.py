from django.shortcuts import render
from .models import Car

def cars_list(request):
    cars = Car.objects.all()
    return render(request, 'transport/cars_list.html', {'cars': cars})
