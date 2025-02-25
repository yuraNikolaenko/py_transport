from django.urls import path, include
from .views import cars_list,generate_trip_report,TripViewSet
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from .views import register
from .views import dashboard  # ✅ Добавляем импорт

# Добавляем объявление router
router = DefaultRouter()
router.register(r'trips', TripViewSet)  # Регистрируем API для поездок

urlpatterns = [
    path('', cars_list, name='cars_list'),
    path("report/trips/", generate_trip_report, name="trip_report"),
    path('api/', include(router.urls)),  # API теперь доступно по /api/trips/
    path("login/", auth_views.LoginView.as_view(template_name="transport/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path("dashboard/", dashboard, name="dashboard"),

]

