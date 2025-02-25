from django.shortcuts import render
from .models import Car
import io
from datetime import datetime
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import Trip
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required  # ✅ Добавляем импорт

@login_required
def cars_list(request):
    cars = Car.objects.all()
    return render(request, 'transport/cars_list.html', {'cars': cars})


def generate_trip_report(request):
    """Генерация отчёта по поездкам в PDF"""

    # Получаем параметры периода из GET-запроса (по умолчанию весь период)
    start_date = request.GET.get("start_date", "2000-01-01")
    end_date = request.GET.get("end_date", datetime.today().strftime("%Y-%m-%d"))

    # Получаем поездки за указанный период
    trips = Trip.objects.filter(date__range=[start_date, end_date])

    # Подсчёт общего пробега и расхода топлива
    total_distance = sum(trip.route.distance_km if trip.route else 0 for trip in trips)
    total_fuel = sum(trip.fuel_consumed for trip in trips)

    # Создаём PDF в памяти
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    # Заголовок отчёта
    title = f"Отчёт по поездкам с {start_date} по {end_date}"
    elements.append(canvas.Canvas(buffer, pagesize=A4).drawString(100, 800, title))

    # Данные для таблицы
    table_data = [["Дата", "Автомобиль", "Водитель", "Пробег (км)", "Расход топлива (л)"]]
    for trip in trips:
        distance = trip.route.distance_km if trip.route else 0
        table_data.append([trip.date, trip.car.brand, trip.driver.full_name, distance, trip.fuel_consumed])

    # Итоги
    table_data.append(["", "", "Итого:", total_distance, total_fuel])

    # Создаём таблицу
    table = Table(table_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    # Создаём PDF
    doc.build(elements)
    buffer.seek(0)

    # Возвращаем PDF в виде файла
    return FileResponse(buffer, as_attachment=True, filename="trip_report.pdf")



# Сериализатор (конвертирует данные в JSON)
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

# API для работы с поездками
class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Разрешаем только авторизованным пользователям


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # После регистрации перенаправляет на вход
    else:
        form = UserCreationForm()
    return render(request, "transport/register.html", {"form": form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    return render(request, "transport/dashboard.html")