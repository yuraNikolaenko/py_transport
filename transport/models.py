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

class Driver(models.Model):
    full_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.full_name

class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    number_plate = models.CharField(max_length=20, unique=True)
    mileage = models.IntegerField()
    status = models.CharField(max_length=20, choices=[("active", "Active"), ("repair", "In Repair")])
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.number_plate})"

class Route(models.Model):
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    distance_km = models.FloatField()

class Trip(models.Model):
    date = models.DateField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)  # Связь с маршрутом
    fuel_consumed = models.FloatField()

    def __str__(self):
        return f"{self.date} - {self.car} - {self.driver}"


class RepairExpense(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()