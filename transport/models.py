from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('dispatcher', 'Диспетчер'),
        ('mechanic', 'Механик'),
        ('driver', 'Водитель'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='transport_users',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='transport_users_permissions',
        blank=True
    )

class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    number_plate = models.CharField(max_length=15, unique=True)
    mileage = models.PositiveIntegerField()
    status = models.CharField(max_length=20)

class Driver(models.Model):
    full_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    license_number = models.CharField(max_length=20)

class Route(models.Model):
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    distance_km = models.FloatField()

class Trip(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    fuel_consumed = models.FloatField()
    date = models.DateField()

class RepairExpense(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()