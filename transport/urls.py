from django.urls import path
from .views import cars_list

urlpatterns = [
    path('', cars_list, name='cars_list'),
]
